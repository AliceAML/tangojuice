from fastapi import FastAPI, Form, HTTPException, Request, File
from fastapi.datastructures import UploadFile
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# https://fastapi.tiangolo.com/advanced/templates/

import youtube_transcript_api._errors
import vocab

import scraper
from anki import generate_anki_cards
from deepl_translate import target_languages

app = FastAPI(
    title="TangoJuice",
    description="This API extracts vocabulary from webpages and classifies them by frequency",
    version="0.1",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", name="Index", description="Homepage")
async def index(request: Request):
    with open("templates/index.html", "r") as f:
        index = f.read()
    return templates.TemplateResponse(
        "index.html", {"request": request, "output_languages": target_languages}
    )


async def extract_vocab_from_form(
    url,
    text,
    srtfile,
    recursive,
    inputLang,
    outputLang,
    nbWords,
    rareWordsOnly,
    noPropNouns,
) -> list:
    """
    Pipeline used in scrape and download_anki to generate the vocabulary using the
    form data.
    """
    print(inputLang, outputLang)
    if inputLang == outputLang[:2].lower():
        raise HTTPException(
            status_code=404, detail="Input and output languages identical"
        )

    if rareWordsOnly != False:
        rareWordsOnly = True
    print("rareWordsOnly", rareWordsOnly)

    title = ""

    if url != None:
        print(f"Scraping page at {url}")
        try:
            text_url, title_url = scraper.scrape(
                url, recursive=recursive, lang=inputLang
            )
            #weird way of handling a 403 status code error
            if isinstance(text_url, int) and not title_url:
                raise HTTPException(status_code=text_url, detail="Access denied. If you are scraping an article, try and copy paste its content in the 'From Text' section of the home page")
            text += text_url
            title += title_url
        except youtube_transcript_api._errors.NoTranscriptFound as e:
            raise HTTPException(status_code=404, detail="Subtitles not found")



    elif srtfile != None:
        print(f"reading srt file {srtfile=}")
        title += srtfile.filename
        srt: bytes = await srtfile.read()
        srt = srt.decode("utf-8")
        text += scraper.get_text_from_srt(srt)


    if text.strip() == "":
        raise HTTPException(status_code=404, detail="No text to parse")
    voc = vocab.make_vocab(
        text,
        input_lang=inputLang.lower(),
        output_lang=outputLang.lower(),
        noPropNouns=noPropNouns,
    )
    vocList = voc.extract_vocab(nb_words=int(nbWords), onlyRareWords=rareWordsOnly)

    return vocList, title


@app.post(
    "/extract",
    name="Extract",
    summary="Returns a list of relevant word objects from a webpage",
    description="""if recursive = true, will also scrap links to the same domain that are on the page""",
)
async def extract(
    request: Request,
    url=Form(default=None),
    text=Form(default=""),
    srtfile: UploadFile = File(default=None),
    recursive=Form(default=False),
    inputLang=Form(...),
    outputLang=Form(...),
    nbWords=Form(...),
    rareWordsOnly=Form(default=False),
    noPropNouns=Form(default=False),
):

    vocList, title = await extract_vocab_from_form(
        url,
        text,
        srtfile,
        recursive,
        inputLang,
        outputLang,
        nbWords,
        rareWordsOnly,
        noPropNouns,
    )
    return templates.TemplateResponse(
        "results_words.html",
        {"request": request, "words": vocList, "url": url, "title": title},
    )


@app.post(
    "/anki",
    name="download_anki",
    summary="downloads the relevant vocabulary in anki format",
)
# source: https://stackoverflow.com/a/61910803
async def download_anki(
    request: Request,
    url=Form(default=None),
    text=Form(default=""),
    srtfile: UploadFile = File(default=None),
    recursive=Form(default=False),
    inputLang=Form(...),
    outputLang=Form(...),
    nbWords=Form(...),
    rareWordsOnly=Form(default=False),
    noPropNouns=Form(default=False),
):
    vocList, title = await extract_vocab_from_form(
        url,
        text,
        srtfile,
        recursive,
        inputLang,
        outputLang,
        nbWords,
        rareWordsOnly,
        noPropNouns,
    )
    stream_anki = generate_anki_cards(vocList, title=title)
    response = StreamingResponse(iter([stream_anki.getvalue()]), media_type="apkg")

    response.headers["Content-Disposition"] = "attachment; filename=tangojuice.apkg"

    return response




"""
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'url=https%3A%2F%2Fwww.lemonde.fr%2Fsociete%2Farticle%2F2021%2F10%2F30%2Fheure-d-hiver-comment-la-suppression-du-changement-d-heure-a-disparu-de-l-agenda-politique-europeen_6100450_3224.html'
  """
