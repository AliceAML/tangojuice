"""Extract text from urls (webpage or youtube video)"""

from tempfile import SpooledTemporaryFile
import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin, urlparse, parse_qs
import srt

import youtube_transcript_api._errors
from youtube_transcript_api import YouTubeTranscriptApi

MAX_NB_LINKS = 50


def youtube_get_text(url: str, lang: str) -> str:
    video_id = parse_qs(urlparse(url).query)["v"][0]
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
    text_only = [elt["text"] for elt in transcript]
    return "\n".join(text_only)


def is_youtube_video(url):
    """source : https://stackoverflow.com/a/65406515"""
    checker_url = "https://www.youtube.com/oembed?url="
    video_url = checker_url + url

    request = requests.get(video_url)

    return request.status_code == 200


def get_text_from_srt(srt_content: str):
    parsed_srt = srt.parse(srt_content)
    text = "\n".join((line.content for line in parsed_srt))
    return text


def scrape(url: str, lang, recursive=False) -> str:
    """
    Returns a string containing the raw text from the webpage.
    If recursive=True, add the raw text of all linked pages from the same site
    """
    print("scrape", url)

    netloc = urlparse(url).netloc
    response = requests.get(url)

    if response.status_code >= 400:
        print(f"Scrape error: {response.status_code} ")
        print("The error will be obvious for the user in the result page")
        return response.status_code, None

    soup = BeautifulSoup(response.text, "lxml")
    title = soup.find("title").text

    # add call to youtube.get_text() for youtube videos !
    # check if it's a youtube video
    if is_youtube_video(url):
        try:
            text = youtube_get_text(url, lang)
        except youtube_transcript_api._errors.NoTranscriptFound as e:
            raise e
    else:
        for elt in soup("noscript"):
            elt.extract()
        for elt in soup("script"):
            elt.extract()

        text = soup.get_text(separator=" ", strip=True)

        if recursive:
            links = [link["href"] for link in soup.find_all("a", attrs={"href": True})]
            inside_links = [  # limited to same netloc to limit nb
                urljoin(url, link)
                for link in links
                if urlparse(link).netloc in (netloc, "")
            ]

            for link in list(set(inside_links))[:MAX_NB_LINKS]:
                try:
                    text += scrape(link, lang=lang)
                except requests.exceptions.InvalidSchema as e:
                    print(e)

    if lang == "zh":
        try:
            text = text.encode("utf-8").decode("gbk")
        except UnicodeDecodeError:
            pass
        try:
            title = title.encode("utf-8").decode("gbk")
        except UnicodeDecodeError:
            pass


    print(text)
    print("title", title)
    return text, title


if __name__ == "__main__":
    text = scrape(
        "https://cn.nytimes.com/business/20211029/china-coal-climate/",
        recursive=False,
        lang="en",
    )
    counts = {
        w: i
        for w, i in sorted(Counter(text.split()).items(), key=lambda x: -x[1])
        if i > 1
    }
    print(counts)
