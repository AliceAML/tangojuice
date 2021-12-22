"""get info from PONS dict https://en.pons.com/p/files/uploads/pons/api/api-documentation.pdf
The POD-API is provided to you directly with a free quota of 1000 reference queries per month"""
import requests
import json
from bs4 import BeautifulSoup
from collections import Counter
from config import PONS_KEY
import sys


def translate(word, src, dest):
    response = requests.get(
        "https://api.pons.com/v1/dictionary",
        headers={"X-Secret": PONS_KEY},
        params={
            "q": word,
            "l": "".join(sorted([src, dest])),
            "in": src,
            "fm": "1",
            "language": dest,
        },  # j'arrive pas à avoir les bonnes langues :(
    )
    # print(response)

    # with open("pons_test.json", "w") as f:
    #     json.dump(response.json(), f, indent=4)

    print(f"'{word}' from {src} to {dest} = ", end="")
    translations = Counter()
    if response:
        r = response.json()
        for entry in r[0]["hits"]:
            for rom in entry["roms"]:
                if rom["headword"].lower() == word.lower():
                    # headword_full = BeautifulSoup(
                    #     rom["headword_full"], "html.parser"
                    # ).get_text()
                    # # print(headword_full)
                    for arab in rom["arabs"]:
                        for translation in arab["translations"]:
                            if 'class="headword">' in translation["source"]:
                                target = BeautifulSoup(
                                    translation["target"], "html.parser"
                                )
                                translations.update([target.contents[0].strip()])
                                # print("\t", target.contents[0])
        translations = {
            k: v for k, v in translations.most_common(3)
        }  # I HARDCODED A MAX NUMBER HERE :o
        print(", ".join(translations.keys()))
    return ", ".join(translations.keys())

    # TODO rajouter un filtre sur pos !


if __name__ == "__main__":
    print(translate(sys.argv[1], src=sys.argv[2], dest=sys.argv[3]))
