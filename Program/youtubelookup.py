import yt_dlp
import json

def lookup_youtube():
    url = input("Enter YouTube channel URL : ").strip()

    if url.startswith("@"):
        url = "https://www.youtube.com/" + url

    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "extract_flat": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
        except Exception as e:
            print("Failed to extract channel:", e)
            return

    print("\nYouTube Channel Lookup")
    print("=" * 60)

    print("Channel name:", info.get("channel"))
    print("Channel ID:", info.get("channel_id"))
    print("Channel URL:", info.get("channel_url"))
    print("Handle:", info.get("uploader_id"))
    print("Description:", info.get("description", "Not public"))
    print("Subscribers:", info.get("channel_follower_count", "Hidden"))
    print("Total views:", info.get("view_count", "Unknown"))
    print("Video count:", info.get("playlist_count", "Unknown"))
    print("Uploader:", info.get("uploader"))

    print("=" * 60)

if __name__ == "__main__":
    lookup_youtube()
