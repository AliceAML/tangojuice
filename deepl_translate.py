import deepl

from config import DEEPL_KEY

translator = deepl.Translator(DEEPL_KEY)


def translate(text, src, dest):
    print(f'Translate "{text}" to {dest}', end="... ")
    if dest == "en":
        dest = "en-US"  # FIXME ne pas comme ça, c'est mal
    res = translator.translate_text(
        text, target_lang=dest.upper(), source_lang=src.upper()
    )
    print(res)
    return res.text
