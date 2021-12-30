import json
import sys
import math
import spacy
from collections import defaultdict
from tqdm import tqdm

MODEL_NAMES = {
    "de": "de_core_news_sm",  # "de_dep_news_trf",
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "ja": "ja_core_news_sm",
    "no": "nb_core_news_sm",
    "zh": "zh_core_web_sm",
}


def convert_freq_list_to_json(file):
    """
    Converts a frequency list to a json file.
    """
    lang = file.split("_")[0]
    print(f"Load {MODEL_NAMES[lang]}")
    nlp = spacy.load(MODEL_NAMES[lang])

    with open(file, "r") as f:
        total = 0
        nb_lines = 0
        for line in f:
            nb_lines += 1
            form, freq = line.split()
            total += int(freq)

    print(f"{total} total words")
    print(f"{nb_lines} lines")
    freqs = {}
    freqs_lemmas = defaultdict(float)
    with open(file, "r") as f:
        for line in tqdm(f, total=nb_lines):
            word, count = line.split()
            count = int(count)
            freqs[word] = int(count) / total

            lemma = nlp(word)[0].lemma_
            freqs_lemmas[lemma] += int(count) / total

    with open(file.replace(".txt", ".json"), "w") as g:
        json.dump(freqs, g, indent=2)

    with open(file.replace(".txt", "_lemmas.json"), "w") as g:
        json.dump(freqs_lemmas, g, indent=2)


def sort_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    print(f"Sorting {file}")
    sorted_data = {
        lemme: freq
        for lemme, freq in sorted(data.items(), key=lambda x: x[1], reverse=True)
    }
    print(list(sorted_data.items())[:10])
    with open(file, "w") as f:
        json.dump(
            sorted_data,
            f,
            indent=2,
        )
    print(f"Sorted {file}")


if __name__ == "__main__":
    if sys.argv[1] == "convert":
        print(f"Convert {sys.argv[2]}")
        convert_freq_list_to_json(sys.argv[2])
    elif sys.argv[1] == "sort":
        print(f"Sort {sys.argv[2]}")
        sort_json(sys.argv[2])
