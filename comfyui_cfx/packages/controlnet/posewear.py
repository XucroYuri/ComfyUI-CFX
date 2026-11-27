"""Search the pose catalog and export one image for an existing workflow."""

import argparse
import json
from pathlib import Path

from pose_library import catalog, load, prompts, resolve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    ls = sub.add_parser("list")
    ls.add_argument("--search", default="")
    for name in ("show", "export"):
        p = sub.add_parser(name)
        p.add_argument("pose")
        p.add_argument("--view", default="auto")
        if name == "export":
            p.add_argument("--out", type=Path, required=True)
            p.add_argument("--cache", type=Path, default=Path.home() / ".cache/posewear-reference")
            p.add_argument("--offline", action="store_true")
    args = parser.parse_args()
    if args.command == "list":
        for row in catalog().values():
            values = [row[k] for k in ("id", "title", "category", "en")]
            if args.search.casefold() in " ".join(values).casefold():
                print("\t".join([*values, ",".join(row["angles"])]))
        return
    row, view, entry = resolve(args.pose, args.view)
    if args.command == "export":
        if args.out.exists():
            parser.error(f"Output already exists: {args.out}")
        image, _, _ = load(args.pose, view, args.cache, online=not args.offline)
        image.save(args.out)
    zh, en = prompts(row, entry)
    print(
        json.dumps(
            dict(
                pose=row["id"], view=view, title=row["title"], source=row["source"], image_url=entry.get("url"), prompt_zh=zh, prompt_en=en
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
