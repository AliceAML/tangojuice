from googletrans import Translator

translator = Translator()


def translate(text, dest):
    print(f"Translate {text} to {dest}")
    trad = translator.translate(text, dest=dest).text
    print(f"\t{text}")
    return trad
