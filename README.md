# YouTube Playlist Subtitle Downloader

Download subtitles from every video in a YouTube playlist and save each subtitle file as `.srt`.

## Requirements

- Python 3.9+
- `ffmpeg` (required by `yt-dlp` to convert subtitles to `.srt`)

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python download_subtitles.py "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

### Options

```bash
python download_subtitles.py "PLAYLIST_URL" \
  --output subtitles \
  --languages en,es \
  --no-auto
```

- `--output`: Directory to store `.srt` files (default: `subtitles`).
- `--languages`: Comma-separated language codes to download (default: `en`).
- `--no-auto`: Disable auto-generated subtitles.
- `--no-manual`: Disable manually uploaded subtitles.

## Notes

- Output files are named with the playlist index and video title, e.g. `01-Video Title.srt`.
- If a video doesn't have subtitles in the requested language(s), it will be skipped.
