"""Pose catalog and local cache shared by the CLI and ComfyUI node."""

import json
from functools import lru_cache
from io import BytesIO
from pathlib import Path
from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

from PIL import Image, ImageOps

ASSETS = Path(__file__).resolve().parent / "pose_assets"
LIMIT = 12 * 1024 * 1024


@lru_cache(maxsize=1)
def catalog():
    rows = json.loads((ASSETS / "catalog.json").read_text(encoding="utf-8"))
    for path in sorted(ASSETS.glob("pose_*.json")):
        rows.append(
            dict(
                id=path.stem,
                title={"pose_step": "跨步展臂", "pose_seated": "坐姿阅读"}[path.stem],
                category="自制骨架",
                framing="全身",
                source="本项目自制 COCO-18 骨架",
                zh={"pose_step": "大步跨出，一侧手臂抬起维持平衡", "pose_seated": "坐在矮凳上，双手靠近膝部"}[path.stem],
                en={"pose_step": "wide stride, arm extended for balance", "pose_seated": "seated on a low stool, hands near knees"}[
                    path.stem
                ],
                angles={"diagram": dict(label="骨架", prompt="", file=path.with_suffix(".png").name)},
            )
        )
    return {row["id"]: row for row in rows}


def labels():
    return {f"{row['id']} | {row['title']} ({row['category']})": row["id"] for row in catalog().values()}


def resolve(pose_id, view):
    row = catalog()[pose_id]
    if view == "auto":
        view = "front" if "front" in row["angles"] else next(iter(row["angles"]))
    if view not in row["angles"]:
        raise ValueError(f"{pose_id}: {view} unavailable. Available: {', '.join(row['angles'])}")
    return row, view, row["angles"][view]


def decode(payload):
    if len(payload) > LIMIT:
        raise ValueError("Reference image exceeds 12 MiB")
    with Image.open(BytesIO(payload)) as image:
        if image.width * image.height > 20_000_000:
            raise ValueError("Reference image exceeds 20 megapixels")
        return ImageOps.exif_transpose(image).convert("RGB")


def approved_url(url):
    p = urlparse(url)
    return p.scheme == "https" and p.netloc == "posewear.pages.dev" and p.path.startswith("/p/i/")


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def load(pose_id, view, cache, *, online=False):
    row, view, entry = resolve(pose_id, view)
    if "file" in entry:
        image = decode((ASSETS / entry["file"]).read_bytes())
    else:
        local = Path(cache) / f"{pose_id}_{view}.webp"
        for option in (local.with_suffix(".png"), local.with_suffix(".jpg"), local.with_suffix(".jpeg"), local):
            if option.is_file():
                if not option.resolve().is_relative_to(Path(cache).resolve()):
                    raise ValueError("Reference path escapes the cache")
                with option.open("rb") as stream:
                    image = decode(stream.read(LIMIT + 1))
                break
        else:
            if not online:
                raise FileNotFoundError(f"Place {local.name} or same-stem PNG/JPEG in {local.parent}")
            url = entry["url"]
            if not approved_url(url):
                raise ValueError("Unexpected source image URL")
            opener = build_opener(NoRedirect())
            with opener.open(Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=25) as response:
                payload = response.read(LIMIT + 1)
            if len(payload) > LIMIT:
                raise ValueError("Reference image exceeds 12 MiB")
            image = decode(payload)
            local.parent.mkdir(parents=True, exist_ok=True)
            with NamedTemporaryFile(dir=local.parent, delete=False) as tmp:
                tmp.write(payload)
            Path(tmp.name).replace(local)
    return image, row, entry


def prompts(row, entry):
    return tuple(
        "，".join(filter(None, (row[key], entry["label"] if key == "zh" else entry["prompt"])))
        if key == "zh"
        else ", ".join(filter(None, (row[key], entry["prompt"])))
        for key in ("zh", "en")
    )
