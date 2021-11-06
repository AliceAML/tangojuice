"""Extract text from subtitle files (srt)"""

from subsceneAPI import subtitle  # ça marche mais ce package est pas top
import os
import zipfile
import srt
from pathlib import Path

SUB_PATH = os.path.relpath("static/subtitles")


def get_text_from_srt(path):
    text = ""
    with open(path, "r", encoding="utf-8") as f:
        parsed_srt = srt.parse(f.read())
        text = "\n".join((line.content for line in parsed_srt))
    return text


# CETTE FONCTION MARCHE PAS VRAIMENT
def get_subtitle_text(title, language, year):
    # DOWNLOAD SUBS
    sub = subtitle.search(
        title=title, year=year
    )  # PAS DE POSSIBILITE DE CHOISIR UN EPISODE !!
    sub.downloadZIP(path=SUB_PATH)

    # UNZIP
    zfiles = Path(SUB_PATH).rglob("*.zip")

    for zfile in zfiles:
        with zipfile.ZipFile(zfile, "r") as zip_ref:
            zip_ref.extractall(SUB_PATH)

    # LOAD STR
    srts = Path(SUB_PATH).rglob("*.srt")
    text = ""
    for srt_file in srts:
        get_text_from_srt(srt_file)

    # DELETE ALL FILES in SUB_PATH
    for file in Path(SUB_PATH).rglob("*"):
        file.unlink()

    return text


if __name__ == "__main__":
    # print(get_subtitle_text("Grey's Anatomy", "english", "2014"))
    # print(
    #     get_subtitle_text(
    #         "The Big Bang Theory - Ninth Season", "english", "2015", season=9, episode=7
    #     )
    # )
    # print(get_subtitle_text("extraction", "2020", "english"))
    # print(get_subtitle_text("Squid Game", "2021", "english", season=1, episode=1))
    print(get_text_from_srt("static/subtitles/Finch 2021 _English.srt"))
