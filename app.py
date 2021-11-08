from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# https://fastapi.tiangolo.com/advanced/templates/

from collections import Counter, namedtuple
import youtube_transcript_api._errors

import scraper

app = FastAPI(
    title="TangoJuice",
    description="This API extracts vocabulary from webpages and classifies them by frequency",
    version="0.1",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get(
    "/",
    name="Index",
)
async def index():
    with open("templates/index.html", "r") as f:
        index = f.read()
    return HTMLResponse(index)


@app.post(
    "/scrape",
    name="Scrape",
    summary="Returns a raw list of words from a webpage",
    description="""if recursive = true, will also scrap links to the same domain that are on the page
    stupid tokenization only""",
    tags=["Routes"],
)
async def scrape(
    request: Request, url=Form(...), recursive=Form(default=False), inputLang=Form(...)
):
    try:
        text = scraper.scrape(url, recursive=recursive, lang=inputLang)
    except youtube_transcript_api._errors.NoTranscriptFound as e:
        raise HTTPException(status_code=404, detail="Subtitles not found")

    Word = namedtuple("Word", ("text", "count"))
    words = [
        Word(w, i)
        for w, i in sorted(Counter(text.split()).items(), key=lambda x: -x[1])
        if i > 1
    ]

    return templates.TemplateResponse(
        "results.html", {"request": request, "words": words}
    )


"""
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'url=https%3A%2F%2Fwww.lemonde.fr%2Fsociete%2Farticle%2F2021%2F10%2F30%2Fheure-d-hiver-comment-la-suppression-du-changement-d-heure-a-disparu-de-l-agenda-politique-europeen_6100450_3224.html'
  """
