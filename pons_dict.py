"""get info from PONS dict https://en.pons.com/p/files/uploads/pons/api/api-documentation.pdf
The POD-API is provided to you directly with a free quota of 1000 reference queries per month"""
import requests
import json
from bs4 import BeautifulSoup

word = "haus"
in_lang = "de"
out_lang = "zh"

response = requests.get(
    "https://api.pons.com/v1/dictionary",
    headers={
        "X-Secret": "268bd32ee83366a32cf3d2ee938d4c1a85bc326a6bf5eacc3e106aa244021aed"
    },
    params={
        "q": word,
        "l": "".join(sorted([in_lang, out_lang])),
        "in": in_lang,
        "fm": "1",
        "language": out_lang,
    },  # j'arrive pas à avoir les bonnes langues :(
)
print(response)

with open("pons_test.json", "w") as f:
    json.dump(response.json(), f, indent=4)

r = response.json()

translations = set()

for entry in r[0]["hits"]:
    for rom in entry["roms"]:
        if rom["headword"].lower() == word.lower():
            headword_full = BeautifulSoup(
                rom["headword_full"], "html.parser"
            ).get_text()
            print(headword_full)
            for arab in rom["arabs"]:
                for translation in arab["translations"]:
                    if 'class="headword">' in translation["source"]:
                        target = BeautifulSoup(
                            translation["target"], "html.parser"
                        ).get_text()
                        print("\t", target)
