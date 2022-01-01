# :beverage_box: TangoJuice
*Vocabulary extractor*

Language learning web app that extracts the vocabulary from a webpage or a video's captions, filters it by difficulty level and automatically creates [Anki](https://apps.ankiweb.net/) flashcards. Available at https://tangojuice.herokuapp.com/

## How to run the API locally

* clone repo
* setup virtual environment. You will need a [Deepl API authorization key](https://www.deepl.com/fr/docs-api/accessing-the-api/authentication/):
    ```console
    python3 -m virtualenv .venv
    source .venv/bin/activate
    pip install -U -r requirements.txt
    export DEEPL_KEY=your-api-key-here
    ```

* start uvicorn 
    ```console
    uvicorn app:app
    ```
* go to [localhost:8000](http://localhost:8000)

FastAPI documentation can be found at [http://localhost:8000/docs](http://localhost:8000/docs)
