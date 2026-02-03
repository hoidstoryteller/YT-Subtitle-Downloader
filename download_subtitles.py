#!/usr/bin/env python3
"""Download subtitles from every video in a YouTube playlist as .srt files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from yt_dlp import YoutubeDL


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download subtitles from every video in a YouTube playlist as .srt files. "
            "Requires yt-dlp and ffmpeg for subtitle conversion."
        )
    )
    parser.add_argument(
        "playlist_url",
        help="YouTube playlist URL (or any URL yt-dlp can read as a playlist)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="subtitles",
        help="Output directory for .srt files (default: subtitles)",
    )
    parser.add_argument(
        "-l",
        "--languages",
        default="en",
        help=(
            "Comma-separated subtitle languages to download (default: en). "
            "Example: en,es,fr"
        ),
    )
    parser.add_argument(
        "--no-auto",
        action="store_true",
        help="Disable auto-generated subtitles (only download manual if available)",
    )
    parser.add_argument(
        "--no-manual",
        action="store_true",
        help="Disable manually uploaded subtitles (only download auto if available)",
    )
    return parser.parse_args()


def build_options(args: argparse.Namespace) -> dict:
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.no_auto and args.no_manual:
        raise ValueError("Cannot disable both auto and manual subtitles.")

    subtitle_langs = [lang.strip() for lang in args.languages.split(",") if lang.strip()]

    return {
        "skip_download": True,
        "writesubtitles": not args.no_manual,
        "writeautomaticsub": not args.no_auto,
        "subtitleslangs": subtitle_langs,
        "convert_subs": "srt",
        "outtmpl": str(output_dir / "%(playlist_index)02d-%(title)s.%(ext)s"),
        "ignoreerrors": True,
        "noplaylist": False,
    }


def main() -> int:
    args = parse_args()
    try:
        ydl_options = build_options(args)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    with YoutubeDL(ydl_options) as ydl:
        result = ydl.download([args.playlist_url])

    return 0 if result == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
