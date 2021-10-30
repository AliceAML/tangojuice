import requests
from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin, urlparse

import tldextract

MAX_NB_LINKS = 50


def scrape(url: str, recursive=False) -> str:
    """
    Returns a string containing the raw text from the webpage.
    If recursive=True, add the raw text of all linked pages from the same site
    """
    print("scrape", url)

    domain = tldextract.extract(url).domain
    netloc = urlparse(url).netloc
    # print(netloc)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")  # html5lib : ignore hidden comments!
    # filtered_soup = [
    #     elt for elt in soup.find_all() if elt.name not in ("script", "noscript")
    # ]

    # for elt in filtered_soup:
    #     text = elt.get_text().strip()
    #     if "Javascript," in text.split():
    #         print(elt.name)
    #         print([parent.name for parent in elt.parents])

    # text = " ".join(filtered_soup)

    for elt in soup("noscript"):
        elt.extract()
    for elt in soup("script"):
        elt.extract()

    text = soup.get_text(separator=" ", strip=True)

    if recursive:
        links = [link["href"] for link in soup.find_all("a", attrs={"href": True})]

        inside_links = [  # limited to same netloc and not same domain to limit nb
            urljoin(url, link)
            for link in links
            if urlparse(link).netloc in (netloc, "")
        ]

        for link in list(set(inside_links))[:MAX_NB_LINKS]:
            text += scrape(link)

    return text


if __name__ == "__main__":
    text = scrape(
        "https://www.wg-gesucht.de/1-zimmer-wohnungen-in-Berlin.8.1.1.0.html",
        recursive=True,
    )
    counts = {w: i for w, i in Counter(text.split()).items() if i > 5}
    print(counts)
