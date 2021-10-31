# :beverage_box: TangoJuice
*Vocabulary extractor*

Language learning web app that extracts the vocabulary from a webpage or a video's captions, filters it by difficulty level and automatically creates Anki flashcards.

[Links and ideas on Notion](https://sturdy-starfish-3ee.notion.site/Projet-API-31a173f329eb45c4acdcfc5e60d851e1)

## How to run the API locally
* clone repo
* setup virtual environment:
    ```console
    python3 -m virtualenv .venv
    source .venv/bin/activate
    pip install -U -r requirements.txt
    ```
* start uvicorn 
    ```console
    uvicorn app:app
    ```
* go to [localhost:8000](http://localhost:8000)

## To-do list

- [ ]  Script python qui prend en entrée du texte brut et une langue et ressort une liste triée par niveau (débutant, intermédiaire, avancé) et par fréquence dans le texte, avec aussi les phrases exemples !
    - [ ]  Idée : créer une classe Word avec des attributs frequence_rank, translation,examples, occurrences… ? Et une classe Vocabulary qui contient tous les words du texte ? Rangés dans les différentes catégories de niveau
- [ ]  Script qui scrape un site et récupère le contenu texte, avec option « récursive »
- [x]  Implémenter la **traduction** des mots et des phrases
- [x]  Faire l’API qui prend le lien  et renvoie un json
- [ ]  créer flashcards Anki
- [ ]  S’occuper de l’interface HTML
- [ ]  Implémenter Youtube et/ou Netflix

**Idées d’amélioration**

- [ ]  Ne pas juste renvoyer des mots…
- [ ]  Renvoyer les informations morphosyntaxiques (avec SpaCy)
