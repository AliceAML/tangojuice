# coding = utf8
from bs4 import BeautifulSoup
import requests

test_string = "A子列居鄭圃，四十年人无識者。國君卿大夫眎之，猶眾庶也。國不足，將嫁於衛。"


def get_yabla_def_and_transcr(hanzi):
    url = (
        "https://chinese.yabla.com/chinese-english-pinyin-dictionary.php?define=將"
        + hanzi
    )
    print(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "lxml")
    definition = {}
    pinyin = []
    for idx, item in enumerate(soup.find_all("div", attrs={"class": "definition"})[:5]):
        print(idx)
        if item.a.string:
            pinyin.append(item.a.string)
        definition[idx + 1] = item.div.string
        print(item.div.string)

    if len(pinyin) > 1:
        print(pinyin)

    return {'pinyin': pinyin,  'definition': definition }


character_cards = {hanzi: get_yabla_def_and_transcr(hanzi) for hanzi in test_string[5] }
for character in character_cards:
    print(character.decode('utf8'))
    print(character_cards[character])