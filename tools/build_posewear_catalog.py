"""Index public PoseWear pose pages without downloading their images."""

import html
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

BASE = "https://posewear.pages.dev"


def text(url):
    with urlopen(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=30) as response:
        return response.read().decode("utf-8")


def clean(source):
    return html.unescape(re.sub(r"<[^>]+>", "", source)).strip()


def parse(url):
    page = text(url)
    slug = url.rstrip("/").rsplit("/", 1)[1]
    title = clean(re.search(r"<h1>(.*?)</h1>", page).group(1))
    fields = list(map(str.strip, clean(re.search(r'<div class="mu">(.*?)</div>', page).group(1)).split(" · ")))
    prompts = [clean(v) for v in re.findall(r"<small>[^<]*提示词[^<]*</small><p>(.*?)</p>", page)]
    angles = {}
    for path, name, prompt in re.findall(r'<li><a href="(/p/i/[^" ]+)">([^<]+)</a> · <code>(.*?)</code></li>', page):
        key = Path(path).stem.rsplit("_", 1)[1]
        angles[key] = dict(label=clean(name), prompt=clean(prompt), url=urljoin(BASE, path))
    if not angles or len(prompts) != 2:
        raise ValueError(f"Incomplete catalog entry: {url}")
    return dict(
        id=slug, title=title, category=fields[-2], framing=" · ".join(fields[:-2]), zh=prompts[0], en=prompts[1], source=url, angles=angles
    )


if __name__ == "__main__":
    sitemap = text(f"{BASE}/sitemap-pose.xml")
    urls = sorted(set(re.findall(r"<loc>(https://posewear\.pages\.dev/pose/(?:full_single|upper80v2)_P\d+/)</loc>", sitemap)))
    with ThreadPoolExecutor(5) as pool:
        rows = list(pool.map(parse, urls))
    if len(rows) != 98:
        raise ValueError(f"Expected 98 entries from this catalog snapshot, got {len(rows)}")
    out = Path(__file__).resolve().parents[1] / "comfyui_cfx/packages/controlnet/pose_assets/catalog.json"
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(rows), sum(len(row["angles"]) for row in rows), out)
