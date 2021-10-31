from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


def get_text(url: str, lang: str) -> str:
    video_id = parse_qs(urlparse(url).query)["v"][0]
    print(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    text_only = [elt["text"] for elt in transcript]
    return "\n".join(text_only)


# to do add possibility to get the translation
# add info about whether it's a generated transcript or a manual transcript
# https://pypi.org/project/youtube-transcript-api/

if __name__ == "__main__":
    print(get_text("https://www.youtube.com/watch?v=cQl6jUjFjp4&t=26s", lang="en"))
