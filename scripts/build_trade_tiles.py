#!/usr/bin/env python3
"""Download trade-accurate photos and apply a consistent Botdude color grade."""

from __future__ import annotations

import io
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "images" / "trades"
SIZE = (800, 640)

# Unsplash photos chosen to match each trade (free to use via Unsplash License)
TRADES: dict[str, tuple[str, str]] = {
    "plumbing": (
        "https://images.unsplash.com/photo-1584622650111-993a426dbbf0?auto=format&fit=crop&w=1200&h=960&q=85",
        "Plumber working under a kitchen sink with pipe wrench",
    ),
    "hvac": (
        "https://images.unsplash.com/photo-1635766318627-02052a997900?auto=format&fit=crop&w=1200&h=960&q=85",
        "HVAC technician servicing an outdoor air conditioning unit",
    ),
    "roofing": (
        "https://images.unsplash.com/photo-1562259949-e8e7689d782a?auto=format&fit=crop&w=1200&h=960&q=85",
        "Roofer installing shingles on a residential roof",
    ),
    "landscaping": (
        "https://images.unsplash.com/photo-1558904541-efe7f83d15a3?auto=format&fit=crop&w=1200&h=960&q=85",
        "Landscaping crew mowing a residential lawn",
    ),
    "contracting": (
        "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&h=960&q=85",
        "General contractor at a residential construction site",
    ),
    "demolition": (
        "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=1200&h=960&q=85",
        "Demolition work with debris and heavy equipment on site",
    ),
    "electrical": (
        "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1200&h=960&q=85",
        "Electrician working on a residential electrical panel",
    ),
    "windows-doors": (
        "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1200&h=960&q=85",
        "Worker installing a window in a home renovation",
    ),
    "concrete": (
        "https://images.unsplash.com/photo-1589939705384-51851320a311?auto=format&fit=crop&w=1200&h=960&q=85",
        "Concrete worker finishing a freshly poured slab",
    ),
    "office-csr": (
        "https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&h=960&q=85",
        "Office team coordinating customer calls and scheduling",
    ),
}


def fetch_image(url: str) -> Image.Image:
    req = urllib.request.Request(url, headers={"User-Agent": "BotdudeTradeTileBuilder/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    return Image.open(io.BytesIO(data)).convert("RGB")


def grade_for_bento(img: Image.Image) -> Image.Image:
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
    for slug, (url, _alt) in TRADES.items():
        print(f"Building {slug}...")
        raw = fetch_image(url)
        tile = grade_for_bento(raw)
        out_path = OUT_DIR / f"{slug}.jpg"
        tile.save(out_path, "JPEG", quality=86, optimize=True, progressive=True)
        print(f"  -> {out_path.relative_to(ROOT)} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
