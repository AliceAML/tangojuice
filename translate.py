from googletrans import Translator
import sys

translator = Translator()


def translate(text, src, dest):
    print(f'Translate "{text}" to {dest}')
    trad = translator.translate(text, dest=dest, src=src).text
    return trad


if __name__ == "__main__":
    print(translate(sys.argv[1], src=sys.argv[2], dest=sys.argv[3]))
