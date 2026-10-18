#!/usr/bin/env python3
"""Check a generated video without watching it: a frame grid, the loop seam and where the motion is.

usage: python3 art/review.py <video.mp4> [frames]

Writes <video>.grid.jpg next to the video and prints:
  - seam: mean pixel difference between the first and last frame (low = loops without a jump)
  - motion per third of the frame (left / middle / right), so a busy text side shows up
"""

import pathlib
import subprocess
import sys
import tempfile

from PIL import Image, ImageChops, ImageDraw, ImageStat


def frames(video, n):
    out = pathlib.Path(tempfile.mkdtemp())
    total = int(subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", str(video)]).decode().strip().strip(","))
    picks = sorted({round(i * (total - 1) / (n - 1)) for i in range(n)})
    expr = "+".join(f"eq(n\\,{p})" for p in picks)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf", f"select='{expr}',scale=480:-1",
                    "-fps_mode", "vfr", str(out / "f%03d.png")], check=True)
    return [Image.open(p).convert("RGB") for p in sorted(out.glob("f*.png"))], picks


def diff(a, b):
    return sum(ImageStat.Stat(ImageChops.difference(a, b)).mean) / 3


def main():
    video = pathlib.Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    ims, picks = frames(video, n)
    w, h = ims[0].size
    cols = 4
    rows = -(-len(ims) // cols)
    grid = Image.new("RGB", (cols * (w + 6), rows * (h + 18)), "white")
    d = ImageDraw.Draw(grid)
    for i, (im, p) in enumerate(zip(ims, picks)):
        x, y = (i % cols) * (w + 6), (i // cols) * (h + 18)
        grid.paste(im, (x, y))
        d.text((x + 3, y + h + 3), f"frame {p}", fill="black")
    dest = video.with_suffix(".grid.jpg")
    grid.save(dest, quality=85)
    print(f"{video.name}: seam {diff(ims[0], ims[-1]):.1f}", end="")
    for name, (x0, x1) in {"left": (0, 1 / 3), "mid": (1 / 3, 2 / 3), "right": (2 / 3, 1)}.items():
        crop = lambda im: im.crop((int(x0 * w), 0, int(x1 * w), h))
        m = sum(diff(crop(ims[i]), crop(ims[i + 1])) for i in range(len(ims) - 1)) / (len(ims) - 1)
        print(f"  {name} {m:.1f}", end="")
    print(f"\n  grid: {dest}")


if __name__ == "__main__":
    main()
