import deepl
import os

translator = deepl.Translator(os.getenv("DEEPL_KEY"))


def translate(text, src, dest):
    print(f'Translate "{text}" to {dest}', end="... ")
    if dest == "en":
        dest = "en-US"  # FIXME ne pas comme ça, c'est mal
    res = translator.translate_text(
        text, target_lang=dest.upper(), source_lang=src.upper()
    )
    print(res)
    return res.text
