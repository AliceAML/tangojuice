# :beverage_box: TangoJuice
*Vocabulary extractor*

Language learning web app that extracts the vocabulary from a webpage or a video's captions, filters it by difficulty level and automatically creates Anki flashcards.

[Links and ideas on Notion](https://sturdy-starfish-3ee.notion.site/Projet-API-31a173f329eb45c4acdcfc5e60d851e1)

[Consignes](https://loicgrobol.github.io/web-interfaces/assignments/projets.html)

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

- [ ]  `vocab.py` extraction du vocab à partir d'une string.
    - [ ] déterminer seuils de "rareté" et des mots à ignorer (trop communs)
    - [ ] résoudre le problème du sentencizer qui fait n'importe quoi
- [ ] Implémenter la **traduction** des mots et des phrases
- [ ] Ajouter possibilité d'envoyer un fichier srt dans l'API
- [ ]  S’occuper de l’interface HTML
    - [ ] Ajouter boutons "Only show rare words"
    - [ ] Traduire interface en anglais
    - [ ] Intégrer nouvelles infos au tableau des résultats
    - [x] Copier les *tabs* de https://validator.w3.org/#validate_by_input
- [ ]  créer flashcards Anki$
- [x]  Script qui scrape un site et récupère le contenu texte, avec option « récursive »
- [x]  Ajouter support Youtube
- [x]  Faire l’API qui prend le lien  et renvoie un json
- [x] Ajouter un input text (pour extraire voc à partir d'un copier-coller)
- [ ] 




**Idées d’amélioration**

- [x]  Ne pas juste renvoyer des mots…
- [x]  Renvoyer les informations morphosyntaxiques (avec SpaCy)
- [ ]  Gestion des entités nommées
- [ ]  Gestion des "cognates" (mots apparentés)
