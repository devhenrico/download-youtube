import re
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import imageio_ffmpeg
import yt_dlp

SUPPORTED_FORMATS = {"mp3", "mp4"}
VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")

def normalize_video_url(url):
    if not isinstance(url, str) or len(url) > 2048:
        return None
    try:
        parsed = urlparse(url.strip())
        hostname = (parsed.hostname or "").lower().removeprefix("www.")
        allowed_port = parsed.port in (None, 80, 443)
    except ValueError:
        return None

    if (parsed.scheme not in ("http", "https") or parsed.username or parsed.password
            or not allowed_port or hostname not in {
                "youtube.com", "youtu.be", "m.youtube.com", "music.youtube.com"
            }):
        return None

    video_id = None
    if hostname == "youtu.be":
        video_id = parsed.path.strip("/")
    elif parsed.path.rstrip("/") == "/watch":
        video_id = parse_qs(parsed.query).get("v", [None])[0]
    else:
        match = re.fullmatch(r"/(?:shorts|live|embed)/([A-Za-z0-9_-]{11})/?", parsed.path)
        if match:
            video_id = match.group(1)

    if not video_id or not VIDEO_ID_PATTERN.fullmatch(video_id):
        return None
    return f"https://www.youtube.com/watch?v={video_id}"

def is_youtube_url(url):
    return normalize_video_url(url) is not None

def _safe_filename(title, formato):
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f\x7f]', "", str(title or "YouTube"))
    name = re.sub(r"\s+", " ", name).strip(" .")[:150].rstrip(" .")
    if not name or name.upper() in {
        "CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        name = "YouTube"
    return f"{name}.{formato}"

def download_media(url, formato, directory):
    video_url = normalize_video_url(url)
    if formato not in SUPPORTED_FORMATS or not video_url:
        raise ValueError("Formato ou URL de vídeo não permitido.")

    output = str(Path(directory) / "%(id)s.%(ext)s")
    options = {
        "outtmpl": output,
        "noplaylist": True,
        "extractor_args": {"youtube": {"player_client": ["android"]}},
        "retries": 5,
        "fragment_retries": 5,
        "socket_timeout": 30,
        "continuedl": True,
        "writethumbnail": True,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "format": "bestaudio/best" if formato == "mp3" else "bv+ba/b",
        "format_sort": ["abr", "asr"] if formato == "mp3" else ["res", "fps", "vbr", "abr"],
        "postprocessors": [],
    }
    if formato == "mp3":
        options["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "320"},
            {"key": "FFmpegMetadata", "add_metadata": True},
            {"key": "EmbedThumbnail"},
        ]
    else:
        options["merge_output_format"] = "mp4"
        options["postprocessors"] = [
            {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"},
            {"key": "FFmpegMetadata", "add_metadata": True},
            {"key": "EmbedThumbnail"},
        ]

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(video_url, download=True)

    if not isinstance(info, dict):
        raise FileNotFoundError("O YouTube não retornou informações do vídeo.")

    path = info.get("filepath")
    result = Path(path) if path else None
    folder = Path(directory).resolve()
    if not result or not result.is_file() or result.suffix.lower() != f".{formato}" or result.resolve().parent != folder:
        candidates = list(folder.glob(f"*.{formato}"))
        result = max(candidates, key=lambda f: f.stat().st_mtime, default=None)
    if result is None or not result.is_file():
        raise FileNotFoundError("O arquivo convertido não foi encontrado.")
    return result, _safe_filename(info.get("title"), formato)
