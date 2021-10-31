# tutos : https://www.youtube.com/playlist?list=PLDnNM3HYR2mUKXci_c20CS8MEfeSr6gOj
# Google API Python client https://github.com/googleapis/google-api-python-client

from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def get_text(url: str, lang: str) -> str:
    video_id = parse_qs(urlparse(url).query)["v"][0]
    print(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    text_only = [elt["text"] for elt in transcript]
    return "\n".join(text_only)


if __name__ == "__main__":
    print(get_text("https://www.youtube.com/watch?v=cQl6jUjFjp4&t=26s", lang="en"))
