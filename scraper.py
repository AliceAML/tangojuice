import requests
from bs4 import BeautifulSoup
from collections import Counter


def scrape(url: str, article_only=False):  ## TODO implement article_only
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    text = soup.get_text(separator=" ", strip=True)
    return text
