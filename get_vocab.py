# coding = utf8
"""
This module implements vocabulary extraction. It is able to perform the extraction from an URL to an article or a video from
anyone of the following domain name:
cn.nytimes.com (chinese new-york times)

For now it just runs on the character level,
token level procesing has yet to be implemented
.. (to be continued: youtube,)
Still very slow

"""

import json
from collections import Counter
import requests
import lxml
from bs4 import BeautifulSoup


global threshold
global punctuation
punctuation = (
    "1２3456789」(.·—，2＿≒＄（。＊１＋＾’！ー？『)＃９％』”＠、＆８３azertyuiopqsdfghjklmwxcvbnnAZERTYUIOPQSDFGHJKLMWXCVBN#*€Ùùéèàç!"
    + "'"
    + '"'
)

threshold = 5

with open("hskHanziList.json", "r") as istream:
    global hsk_voc
    hsk_voc = json.load(istream)



def squeeze_all_from_url(url):
    html = requests.get(url)
    # insert a try except
    soup = BeautifulSoup(html.text, "lxml")
    # extracting the raw paragraph while making sure we are note extracting the images captions
    raw_text = "\n".join(
        [
            paragraph.text
            if not paragraph.find("span") and not paragraph.find("cite")
            else " "
            for paragraph in soup.find_all("div", class_="article-paragraph")
        ]
    )
    hanzi_list = set(raw_text)
    # the above extract the single characters but does not tokenize it properly.
    nlp = spacy.load("zh_core_web_sm")
    print("spacy processing:\n")
    doc = nlp(raw_text)
    print("type doc:\n")
    hanzi_list = [
        hanzi
        for hanzi in hanzi_list
        if get_hsk_level(hanzi) > threshold and hanzi not in punctuation
    ]
    # Add an option: if text is too long refuse it
    # if the proportion of level above threshold is too high, tell the user to choose an easier text
    return infos_and_levels(hanzi_list)


def get_yabla_def_and_transcr(hanzi_or_word):
    url = "https://chinese.yabla.com/chinese-english-pinyin-dictionary.php"
    html = requests.get(url, params={"define": hanzi_or_word})
    soup = BeautifulSoup(html.text, "lxml")
    definition = {}
    pinyin = []
    for idx, item in enumerate(soup.find_all("div", attrs={"class": "definition"})[:5]):
        if item.span.string:
            pinyin.append(item.span.string)
        definition[idx + 1] = item.div.string
        if len(definition) >= 2:
            break

    return {"pinyin": pinyin, "definition": definition}


def get_hsk_level(character):
    for level in hsk_voc:
        if character in hsk_voc[level]:
            return int(level)
    return 7


'''
input: raw text (str)
out: dict of dict. 1st Key: character  2nd keys frequency, level, translations

'''

def infos_and_levels(raw_text):

    occurencies = Counter(raw_text)
    real_length = len(raw_text) - occurencies[" "]
    del occurencies[" "]

    char_info = {
        character: {
            "frequency": occurencies[character] / real_length,
            "hsk level": get_hsk_level(character),
            "translation": get_yabla_def_and_transcr(character),
        }
        for character in set(raw_text)
    }
    levels = Counter(char_info[w]["hsk level"] for w in char_info)
    levels = {difficulty: occ / len(raw_text) for difficulty, occ in levels.items()}
    return char_info, occurencies, levels


if __name__ == "__main__":
    # test_text = "子列居鄭圃，四十年人无識者。乎？」子列子笑曰：「壺子何言哉？雖然，夫子嘗語伯昏瞀人，吾側聞之，試以告女。其言曰：有生不生，有化不化。不生者能生生，不化者能化化。生者不能不生，化者不能不化，故常生常化。常生常化者，无時不生，无時不化。陰陽爾，四時爾，不生者疑獨，不化者往復。往復，其際不可終；疑獨，其道不可窮。《黃帝書》曰：「谷神不死，是謂玄牝。玄牝之門，是謂天地之根。綿綿若存，用之不勤。」故生物者不生，化物者不化。自生自化，自形自色，自智自力，自消自息。謂之生化、形色、智力、消息者，非也。"
    article_url = "https://cn.nytimes.com/business/20211029/china-coal-climate/"
    char_info, occurencies, levels = squeeze_all_from_url(article_url)
