#!/usr/bin/env python3
"""Generate artwork drafts on fal.ai and keep a record of every paid call.

usage: python3 art/gen.py art/jobs/<job>.json [--force]

A job file names a scene, a prompt and one or more runs (model + settings).
Each run is sent to fal's queue, the outputs are saved to art/out/<scene>/<job>/,
and one line per run is appended to art/ledger.csv with its estimated cost.
A job that already has output is not sent again unless --force is given,
so re-running a command by accident never spends credit twice.

The API key is read from ~/.config/fal/key and never printed.
"""

import base64
import csv
import datetime
import json
import pathlib
import sys
import time
import urllib.request

ART = pathlib.Path(__file__).resolve().parent
KEY = (pathlib.Path.home() / ".config/fal/key").read_text().strip()
QUEUE = "https://queue.fal.run/"


def call(url, body=None):
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"},
        method="POST" if body is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def run(endpoint, payload, timeout=900):
    sub = call(QUEUE + endpoint, payload)
    rid = sub["request_id"]
    start = time.time()
    while True:
        status = call(sub["status_url"])["status"]
        if status == "COMPLETED":
            return rid, call(sub["response_url"])
        if time.time() - start > timeout:
            raise TimeoutError(f"{endpoint} request {rid} still {status} after {timeout}s")
        time.sleep(3)


def data_uri(path):
    """A local reference image, inlined so it never needs uploading anywhere else."""
    p = ART / path
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def upload(path):
    """Put a local file (e.g. a video too big to inline) on fal's storage and return its URL."""
    p = ART / path
    mime = {".mp4": "video/mp4", ".png": "image/png"}.get(p.suffix.lower(), "image/jpeg")
    init = call("https://rest.alpha.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3",
                {"content_type": mime, "file_name": p.name})
    req = urllib.request.Request(init["upload_url"], data=p.read_bytes(), method="PUT",
                                 headers={"Content-Type": mime})
    urllib.request.urlopen(req, timeout=300).read()
    return init["file_url"]


def resolve(value):
    if isinstance(value, dict):
        return {k: resolve(v) for k, v in value.items()}
    if isinstance(value, list):
        return [resolve(v) for v in value]
    if isinstance(value, str) and value.startswith("file:"):
        return data_uri(value[5:])
    if isinstance(value, str) and value.startswith("upload:"):
        return upload(value[7:])
    return value


def outputs(result):
    """The media URLs in a fal result, whatever the model calls them."""
    found = []
    for key in ("masks", "images", "image", "video", "videos"):
        val = result.get(key)
        for item in val if isinstance(val, list) else [val] if val else []:
            found.append(item["url"])
    return found


def sheet(files, dest):
    """One contact sheet per job, so a batch can be judged at a glance."""
    from PIL import Image, ImageDraw
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im.thumbnail((640, 640))
        thumbs.append((f.name, im))
    cols = 4
    w = max(t.width for _, t in thumbs)
    h = max(t.height for _, t in thumbs) + 24
    rows = -(-len(thumbs) // cols)
    out = Image.new("RGB", (cols * w + (cols + 1) * 8, rows * h + (rows + 1) * 8), "white")
    draw = ImageDraw.Draw(out)
    for i, (name, im) in enumerate(thumbs):
        x, y = 8 + (i % cols) * (w + 8), 8 + (i // cols) * (h + 8)
        out.paste(im, (x, y))
        draw.text((x + 4, y + im.height + 6), name, fill="black")
    out.save(dest, quality=90)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    job_path = pathlib.Path(args[0])
    job = json.loads(job_path.read_text())
    out = ART / "out" / job["scene"] / job_path.stem
    if out.exists() and not force:
        sys.exit(f"{out} already exists; pass --force to spend credit on it again")
    out.mkdir(parents=True, exist_ok=True)

    saved = []
    ledger = ART / "ledger.csv"
    new_ledger = not ledger.exists()
    for r in job["runs"]:
        # a run may add its own scene to the job's shared prompt
        payload = {"prompt": " ".join(filter(None, [job["prompt"], r.get("prompt")])), **r["input"]}
        if r.get("refs"):
            payload["image_urls"] = [data_uri(p) for p in r["refs"]]
        # image fields anywhere in the input (first/last frame, keyframe lists) can point at a
        # local file as "file:<path>" (inlined) or "upload:<path>" (put on fal storage)
        payload = resolve(payload)
        print(f"→ {r['label']}  ({r['endpoint']}, est ${r['est_cost_usd']:.2f})", flush=True)
        rid, result = run(r["endpoint"], payload)
        record = {**payload, **r["input"]}             # keep file paths, not inlined image data
        if r.get("refs"):
            record["image_urls"] = r["refs"]
        (out / f"{r['label']}.json").write_text(json.dumps({"request_id": rid, "input": record, "result": result}, indent=2))
        for i, url in enumerate(outputs(result), 1):
            ext = url.rsplit(".", 1)[-1].split("?")[0][:4] or "png"
            dest = out / f"{r['label']}-{i}.{ext}"
            urllib.request.urlretrieve(url, dest)
            saved.append(dest)
            print(f"   saved {dest.relative_to(ART.parent)}")
        with ledger.open("a", newline="") as f:
            w = csv.writer(f)
            if new_ledger:
                w.writerow(["date", "scene", "job", "label", "endpoint", "outputs", "est_cost_usd", "request_id"])
                new_ledger = False
            w.writerow([datetime.date.today().isoformat(), job["scene"], job_path.stem, r["label"],
                        r["endpoint"], len(outputs(result)), r["est_cost_usd"], rid])

    images = [p for p in saved if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")]
    if images:
        sheet(images, out / "sheet.jpg")
        print(f"contact sheet: {(out / 'sheet.jpg').relative_to(ART.parent)}")


if __name__ == "__main__":
    main()
