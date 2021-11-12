from fastapi import FastAPI, Form, HTTPException, Request, File
from fastapi.datastructures import UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# https://fastapi.tiangolo.com/advanced/templates/

from collections import Counter, defaultdict, namedtuple
import youtube_transcript_api._errors
import vocab

import scraper
import export_vocab

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
    return templates.TemplateResponse("index.html", {"request": request})


@app.post(
    "/scrape",
    name="Scrape",
    summary="Returns a raw list of words from a webpage",
    description="""if recursive = true, will also scrap links to the same domain that are on the page
    stupid tokenization only""",
    tags=["Routes"],
)
async def scrape(
    request: Request,
    url=Form(default=None),
    text=Form(default=None),
    srtfile: UploadFile = File(default=None),
    recursive=Form(default=False),
    inputLang=Form(...),
    outputLang=Form(...),
    nbWords=Form(...),
):
    if url != None:
        try:
            text = scraper.scrape(url, recursive=recursive, lang=inputLang)
        except youtube_transcript_api._errors.NoTranscriptFound as e:
            raise HTTPException(status_code=404, detail="Subtitles not found")
    elif srtfile != None:
        print(f"{srtfile=}")  # FIXME this is just a string !
        # print(file.file)
        srt: bytes = await srtfile.read()  # TODO extract from srt file
        srt = srt.decode("utf-8")
        text = scraper.get_text_from_srt(srt)

    print(text)
    voc = vocab.make_vocab(text, lang=inputLang)
    vocList = voc.extract_vocab(nb_words=int(nbWords))
    return templates.TemplateResponse(
        "results_words.html", {"request": request, "words": vocList}
    )


@app.post(
    "get selected vocab",
    name="selected_vocab",
    summary="preprocesses the selected vocab before flashcard selection",
    tags=["Routes"],
)
async def selected_vocab(
    request: Request,
):

    return templates.TemplateResponse(
        "exported.html", {"request": request, "word_list": word_list}
    )


@app.post(
    "/export_vocab",
    name="export_vocab",
    summary="exports the selected vocabulary (hopefully into flashcards)",
    description="""if select all = true, will return the whole vocab""",
    tags=["Routes"],
)
async def export_vocab(request: Request, word_list=Form(...)):

    return templates.TemplateResponse(
        "exported.html", {"request": request, "word_list": word_list}
    )


"""
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'url=https%3A%2F%2Fwww.lemonde.fr%2Fsociete%2Farticle%2F2021%2F10%2F30%2Fheure-d-hiver-comment-la-suppression-du-changement-d-heure-a-disparu-de-l-agenda-politique-europeen_6100450_3224.html'
  """
