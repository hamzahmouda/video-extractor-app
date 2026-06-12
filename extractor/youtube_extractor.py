import yt_dlp
from datetime import datetime


def format_duration(seconds):
    if not seconds:
        return ""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y%m%d").strftime("%Y-%m-%d")
    except:
        return date_str
def extract_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    data = {
        "Titre": info.get("title"),
        "Durée": format_duration(info.get("duration")),
        "Chaîne": info.get("uploader"),
        "Date": format_date(info.get("upload_date")),
        "Vues": info.get("view_count"),
        "Description": info.get("description"),
        "Tags": ", ".join(info.get("tags", [])),
        "Thumbnail": info.get("thumbnail"),
        "URL": url
    }

    return data