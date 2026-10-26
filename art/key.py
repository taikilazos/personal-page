#!/usr/bin/env python3
"""Turn a green-screen loop into a see-through sprite for the website.

usage: python3 art/key.py <green.mp4> <out-dir> <name> <width> [frames]

Finds the creature's bounding box over the whole loop, crops to it, keys out the
green, and writes <name>.webm (VP9 with alpha, Chrome/Firefox), <name>.mov (HEVC
with alpha, Safari) and <name>.webp (the first frame, as a poster). Also prints
the box as fractions of the source frame, so the page can place the sprite.
"""

import json
import pathlib
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image


def frames(src, n):
    tmp = pathlib.Path(tempfile.mkdtemp())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"select='not(mod(n\\,{n}))'",
                    "-fps_mode", "vfr", str(tmp / "f%03d.png")], check=True)
    return [np.asarray(Image.open(p).convert("RGB")).astype(int) for p in sorted(tmp.glob("f*.png"))]


def main():
    src, out, name, width = sys.argv[1], pathlib.Path(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    count = sys.argv[5] if len(sys.argv) > 5 else None
    out.mkdir(parents=True, exist_ok=True)
    shots = frames(src, 12)
    h, w = shots[0].shape[:2]
    key = np.median(np.concatenate([s[:40, :40].reshape(-1, 3) for s in shots]), axis=0).astype(int)
    solid = np.zeros((h, w), bool)
    for s in shots:
        solid |= np.abs(s - key).sum(2) > 90
    ys, xs = np.nonzero(solid)
    pad = 16
    x0, x1 = max(0, xs.min() - pad), min(w, xs.max() + pad)
    y0, y1 = max(0, ys.min() - pad), min(h, ys.max() + pad)
    cw, ch = (x1 - x0) // 2 * 2, (y1 - y0) // 2 * 2
    hexkey = "0x%02X%02X%02X" % tuple(key)
    vf = (f"crop={cw}:{ch}:{x0}:{y0},chromakey={hexkey}:0.13:0.06,"
          f"despill=type=green:mix=0.6:expand=0.1,scale={width}:-2:flags=lanczos")
    limit = ["-frames:v", count] if count else []
    run = lambda *a: subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *limit, "-an", *a], check=True)
    run("-vf", vf + ",format=yuva420p", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "34",
        "-row-mt", "1", "-auto-alt-ref", "0", str(out / f"{name}.webm"))
    run("-vf", vf + ",format=bgra", "-c:v", "hevc_videotoolbox", "-allow_sw", "1",
        "-alpha_quality", "0.8", "-q:v", "55", "-tag:v", "hvc1", str(out / f"{name}.mov"))
    poster = pathlib.Path(tempfile.mkdtemp()) / "poster.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-frames:v", "1", "-vf", vf + ",format=rgba",
                    str(poster)], check=True)
    Image.open(poster).save(out / f"{name}.webp", "WEBP", quality=85, method=6)
    box = {"x": round(x0 / w, 4), "y": round(y0 / h, 4), "w": round(cw / w, 4), "h": round(ch / h, 4)}
    sizes = {p.name: p.stat().st_size // 1024 for p in out.glob(f"{name}.*")}
    print(json.dumps({"name": name, "key": hexkey, "box": box, "kb": sizes}))


if __name__ == "__main__":
    main()
