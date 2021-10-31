# coding = utf8
import json
from collections import Counter
import requests
import lxml
from bs4 import BeautifulSoup


with open("hskHanziList.json", "r") as istream:
    global hsk_voc
    hsk_voc = json.load(istream)


def squeeze_all_from_url(url):
    html = requests.get(url)
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
    #the above extract the single characters but does not tokenize it properly.
    # we will add this functionality later.
    print(raw_text)
    # return char_infos_text_levels(raw_text)


def get_yabla_def_and_transcr(hanzi):
    url = "https://chinese.yabla.com/chinese-english-pinyin-dictionary.php"
    html = requests.get(url, params={"define": hanzi})
    requests.get(
        "https://api.github.com/search/repositories",
        params={"q": "requests+language:python"},
    )
    soup = BeautifulSoup(html.text, "lxml")
    definition = {}
    pinyin = []
    for idx, item in enumerate(soup.find_all("div", attrs={"class": "definition"})[:5]):
        if item.span.string:
            pinyin.append(item.span.string)
        definition[idx + 1] = item.div.string

    return {"pinyin": pinyin, "definition": definition}


def get_hsk_level(character):
    for level in hsk_voc:
        if character in hsk_voc[level]:
            return level
    return 7


def char_infos_text_levels(raw_text):
    occurencies = Counter(raw_text)
    real_length = len(test_text) - occurencies[" "]
    del occurencies[" "]
    char_info = {
        w: {
            "frequency": occurencies[w] / real_length,
            "hsk level": get_hsk_level(w),
            "translation": get_yabla_def_and_transcr(w),
        }
        for w in raw_text
    }
    levels = Counter(w["hsk level"] for w in char_info)
    levels = {difficulty: occ / len(raw_text) for difficulty, occ in levels.items()}
    return char_info, occurencies


if __name__ == "__main__":
    test_text = "子列居鄭圃，四十年人无識者。乎？」子列子笑曰：「壺子何言哉？雖然，夫子嘗語伯昏瞀人，吾側聞之，試以告女。其言曰：有生不生，有化不化。不生者能生生，不化者能化化。生者不能不生，化者不能不化，故常生常化。常生常化者，无時不生，无時不化。陰陽爾，四時爾，不生者疑獨，不化者往復。往復，其際不可終；疑獨，其道不可窮。《黃帝書》曰：「谷神不死，是謂玄牝。玄牝之門，是謂天地之根。綿綿若存，用之不勤。」故生物者不生，化物者不化。自生自化，自形自色，自智自力，自消自息。謂之生化、形色、智力、消息者，非也。"
    article_url = "https://cn.nytimes.com/business/20211029/china-coal-climate/"
    squeeze_all_from_url(article_url)
