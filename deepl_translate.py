import deepl
import os

translator = deepl.Translator(os.getenv("DEEPL_KEY"))

target_languages = translator.get_target_languages()


def translate(text, src, dest):
    print(f'Translate "{text}" to {dest}', end="... ")
    res = translator.translate_text(
        text, target_lang=dest.upper(), source_lang=src.upper()
    )
    print(res)
    return res.text
