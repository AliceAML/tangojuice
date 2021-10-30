import pathlib
from fastapi import FastAPI, Form
from pydantic import BaseModel
import spacy
from fastapi.responses import HTMLResponse
from collections import Counter

import scraper

app = FastAPI(
    title="TangoJuice",
    description="This API extracts vocabulary from webpages and classifies them by frequency",
    version="0.1",
)


@app.post(
    "/scrape",
    name="Scrape",
    summary="Returns a raw list of words from a webpage",
    description="""if recursive = true, will also scrap links to the same domain that are on the page
    stupid tokenization only""",
    tags=["Routes"],
)
async def scrape(url=Form(...), recursive=False):
    text = scraper.scrape(url, recursive=recursive)
    counts = {
        w: i for w, i in Counter(text.split()).items() if i > 5
    }  # tokenizer nul juste pour tester
    return counts


"""
curl -X 'POST' \
  'http://localhost:8000/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'url=https%3A%2F%2Fwww.lemonde.fr%2Fsociete%2Farticle%2F2021%2F10%2F30%2Fheure-d-hiver-comment-la-suppression-du-changement-d-heure-a-disparu-de-l-agenda-politique-europeen_6100450_3224.html'
  """
