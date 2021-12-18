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
    - [ ] refaire les json de fréquence avec les vraies fréquences relatives
    - [ ] ou trouver des [fréquences](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists) par lemmes pour fr, en, de, no ?
    - [ ] déterminer seuils de "rareté" et des mots à ignorer (trop communs)
    - [ ] ajouter un attribut "formes"
    - [ ] résoudre le problème du sentencizer qui fait n'importe quoi
    - [ ]  Gestion des "cognates" (mots apparentés)
    - [ ] Transcription en pinyin / romaji
    - [ ] si c'est pas kanji, ça dégage
- [ ] Implémenter la **traduction** des mots et des phrases
    - [ ] Trouver une API pour les mots (Wikitonary?)
    - [ ] Pour les phrases, implémenter avec `googletrans`
- [ ]  S’occuper de l’interface HTML
    - [ ] Ajouter boutons "Only show rare words"
    - [ ] Traduire interface en anglais
    - [ ] Ajouter les options de langues à la page index. Pour la langue de traduction, automatiser. Astuce : `from googletrans import LANGUAGES`
    - [ ] Ajouter menu d'export qui se déplace avec le scroll
    - [ ] Intégrer nouvelles infos au tableau des résultats
    - [x] Copier les *tabs* de https://validator.w3.org/#validate_by_input
- [ ]  créer flashcards Anki
    - [ ] sélection des mots
    - [ ] création d'un fichier de flashcards
    - [ ] upload du fichier
- [x] Ajouter possibilité d'envoyer un fichier srt dans l'API
- [x]  Script qui scrape un site et récupère le contenu texte, avec option « récursive »
- [x]  Ajouter support Youtube
- [x]  Faire l’API qui prend le lien  et renvoie un json
- [x] Ajouter un input text (pour extraire voc à partir d'un copier-coller)
- [ ] Vérifier que l’utilisateur a bien mis la bonne langue (lui demander de vérifier)
- [ ] Gérer la différence entre le chinois tradi (tw) et le chinois simplifié aka vérifier si spacy le fait


**Idées d’amélioration**

- [x]  Ne pas juste renvoyer des mots…
- [x]  Renvoyer les informations morphosyntaxiques (avec SpaCy)
- [ ]  Gestion des entités nommées
