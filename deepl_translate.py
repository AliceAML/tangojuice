import deepl
import os

try:
    translator = deepl.Translator(os.getenv("DEEPL_KEY"))
except:
    print(
        """Error: No DEEPL_KEY found
    get your key here:
    https://www.deepl.com/fr/docs-api/accessing-the-api/authentication/
    add it with:
    export DEEPL_KEY=your-api-key-here
    """
    )

target_languages = translator.get_target_languages()


def translate(text, src, dest):
    print(f'Translate "{text}" to {dest}', end="... ")
    res = translator.translate_text(
        text, target_lang=dest.upper(), source_lang=src.upper()
    )
    print(res)
    return res.text
