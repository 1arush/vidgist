import re
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable

def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def fetch_transcript(video_id: str) -> str:
    api = YouTubeTranscriptApi()
    try:
        print(f"Fetching transcript for video ID: {video_id}")
        fetched = api.fetch(video_id)
        texts = [snippet.text for snippet in fetched]
        print(f"Fetched {len(texts)} snippets for video {video_id}")
        return " ".join(texts)
    except TranscriptsDisabled as e:
        raise RuntimeError(f"Transcripts disabled for video {video_id}")
    except NoTranscriptFound as e:
        raise RuntimeError(f"No transcript found for video {video_id}")
    except VideoUnavailable as e:
        raise RuntimeError(f"Video {video_id} unavailable")
    except Exception as e:
        raise RuntimeError(f"Could not fetch transcript for {video_id}: {e}")

def combine_transcripts(video_urls: list) -> str:
    combined = ""
    for url in video_urls:
        vid = extract_video_id(url)
        if not vid:
            print(f"Warning: invalid URL {url}")
            continue
        try:
            text = fetch_transcript(vid)
            combined += " " + text
        except Exception as e:
            print(f"Warning: failed for video {vid} - {e}")
    return combined
