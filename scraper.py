import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin, urlparse

import youtube

MAX_NB_LINKS = 50


def is_youtube_video(url):
    """source : https://stackoverflow.com/a/65406515"""
    checker_url = "https://www.youtube.com/oembed?url="
    video_url = checker_url + url

    request = requests.get(video_url)

    return request.status_code == 200


def scrape(url: str, lang, recursive=False) -> str:
    """
    Returns a string containing the raw text from the webpage.
    If recursive=True, add the raw text of all linked pages from the same site
    """
    print("scrape", url)

    netloc = urlparse(url).netloc

    # add call to youtube.get_text() for youtube videos !
    # check if it's a youtube video
    if is_youtube_video(url):
        text = youtube.get_text(url, lang)
    else:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")

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
                    text += scrape(link)
                except requests.exceptions.InvalidSchema as e:
                    print(e)

    return text


if __name__ == "__main__":
    text = scrape(
        "https://www.youtube.com/watch?v=cQl6jUjFjp4&t=26s", recursive=False, lang="en"
    )
    counts = {w: i for w, i in Counter(text.split()).items() if i > 5}
    print(counts)
