import json
import sys
import math


def convert_freq_list_to_json(file):
    """
    Converts a frequency list to a json file.
    """

    freqs = {}
    with open(file, "r") as f:
        total = 0
        for line in f:
            total += int(line.split()[1])

    print(f"{total} total words")

    with open(file, "r") as f:
        for line in f:
            word, count = line.split()
            count = int(count)
            freqs[word] = int(count) / total

    with open(file.replace(".txt", ".json"), "w") as g:
        json.dump(freqs, g, indent=2)


print(f"Convert {sys.argv[1]}")
convert_freq_list_to_json(sys.argv[1])
# result = json.load(open(sys.argv[1].replace(".txt", ".json"), "r"))
