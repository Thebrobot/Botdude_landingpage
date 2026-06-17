#!/usr/bin/env python3
"""Grade and resize showcase tile sources for the built-deployments grid."""

from __future__ import annotations

import io
import sys
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "showcase"
SIZE = (800, 550)

SHOWCASE_TILES: dict[str, tuple[str, str]] = {
    "agent-broski": (
        "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&h=825&q=85",
        "Home service dispatcher with headset coordinating inbound calls and bookings",
    ),
    "after-hours": (
        "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&h=825&q=85",
        "Empty dispatch desk at night with active monitors and moonlit windows",
    ),
}


def fetch_image(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers={"User-Agent": "BotdudeShowcaseTileBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return Image.open(io.BytesIO(data)).convert("RGB")


def grade_for_showcase(img: Image.Image) -> Image.Image:
    cropped = ImageOps.fit(img, SIZE, method=Image.Resampling.LANCZOS)
    cropped = ImageEnhance.Contrast(cropped).enhance(1.08)
    cropped = ImageEnhance.Color(cropped).enhance(0.88)
    cropped = ImageEnhance.Brightness(cropped).enhance(0.82)

    overlay = Image.new("RGBA", SIZE, (2, 6, 23, 0))
    pixels = overlay.load()
    w, h = SIZE
    for y in range(h):
        t = y / max(h - 1, 1)
        alpha = int(35 + (165 * t))
        cyan = int(18 * (1 - t))
        for x in range(w):
            pixels[x, y] = (2 + cyan, 6 + cyan, 23 + cyan, alpha)

    base = cropped.convert("RGBA")
    graded = Image.alpha_composite(base, overlay).convert("RGB")
    return ImageEnhance.Sharpness(graded).enhance(1.05)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, (url, _alt) in SHOWCASE_TILES.items():
        print(f"Building {slug}...")
        raw = fetch_image(url)
        tile = grade_for_showcase(raw)
        out_path = OUT_DIR / f"{slug}.jpg"
        tile.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"  -> {out_path.relative_to(ROOT)} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    try:
        main()
    except ModuleNotFoundError:
        print("Install Pillow first: pip install pillow", file=sys.stderr)
        sys.exit(1)
