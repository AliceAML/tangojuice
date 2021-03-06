# Projet interface web

[Consignes](https://loicgrobol.github.io/web-interfaces/assignments/projets.html)

## Objectifs du projet

Créer une application web qui extrait du vocabulaire d'un site web, texte ou fichier de sous-titre afin de permettre le pré-apprentissage du vocabulaire à des apprenants de niveau intermédiaire ou avancé.

## Données et dépendances

[Listes de fréquences](https://github.com/hermitdave/FrequencyWords) (licence MIT) calculées à partir du [corpus OpenSubtitles 2018](https://opus.nlpl.eu/OpenSubtitles2018.php).



## Méthodologie

### Répartition du travail
Nous avons réalisé des points réguliers lors desquels nous avons présenté notre avancement l'un à l'autre et intégré les nouveautés dans le code. Le code était partagé via un dossier sur GitHub. Nous tenions à jour une liste des tâches à réaliser dans le fichier `README` de notre dossier GitHub.

### Identification des problèmes
- Comment sélectionner les mots à extraire ? 

  On voulait partir des listes de niveaux CECRL, ou des listes de vocabulaires correspondant à des niveaux de test de langues (HSK pour le chinois et JLPT pour le japonais). Mais après tout la fréquence paraissait une mesure suffisante pour évaluer la difficulté d’un mot. De plus nous avons trouvé des [listes](https://github.com/hermitdave/FrequencyWords) de mots (lemmes!) et leur fréquence, dans un format uniforme pour toutes les langues. 

  Deuxièmement que faire des formes rare d’un mot par ailleur fréquent. Par exemple “serions” est une occurence relativement rare du lemme le plus fréquent du français. Faut-il l’extraire? De fait nous avons lemmatisé la liste de fréquence si bien que serions n’est pas extrait.

- Comment accélérer le traitement du vocabulaire ? Le chargement du modèle SpaCy est la partie la plus longue du traitement du fichier, malheureusement il n'a pas été possible de charger tous les modèles au démarrage de l'application, car la mémoire disponible sur Heroku était insuffisante. De plus, comme l'application se met en veille, cela rendrait son redémarrage encore plus lent.

- Quelles heuristiques pour nettoyer a minima les fichiers HTML parsés avec beautifulsoup? Pour l’instant on se débarasse des balises script et no script. En tous les cas extraire à partir d’une url produit bien sur plus de bruit que l’extraction depuis un fichier srt sélectionné par l’utilisateur.

  

  

### Etapes du projet

Nous avons commencé par réaliser des versions initiales de l'algorithme d'extraction du vocabulaire (modèle), et de l'API (controlleur) qui permet d'interagir avec cet algorithme. Nous avons également commencé à développer l'interface visuelle (vue) dès le début du projet. Cet aller-retour permanent entre interface utilisateur et algorithme nous a permis de mieux comprendre quelles fonctionnalités seraient utiles à l'utilisateur.rice.

Nous avons ensuite progressivement amélioré ces trois volets de notre projet afin d'améliorer nos résultats et leur présentation.

## Implémentation





### Design pattern

Nous avons essayé de suivre le *design pattern* **Modèle/Vue/Controleur**.
* `app.py` : **controleur** FastAPI qui fait appel aux fonctions de *scraping* et de création du vocabulaire puis les envoie à la **vue** (contenue dans les *templates* `Jinja2`)
* `vocab.py`: **modèle** principal, qui contient la définition des objets `Word` et `Vocabulary`. Le texte est parsé avec SpaCy et chaque nouveau mot est ajouté au vocabulaire, avec son lemme, sa catégorie morphosyntaxique, etc. puis une liste des mots les plus pertinents est retenue en triant le vocabulaire par fréquence dans la liste de fréquence, puis par fréquence inverse dans le document.
    * `deepl_translate.py`: appelé par `vocab.py` après l'extraction de la liste de mots finales
* `scraper.py` : extrait le texte d'un site, d'une vidéo youtube ou d'un fichier `srt` 

### Déploiement sur Heroku
Notre application est automatiquement déployée sur Heroku à chaque mise à jour de la branche `main`. Elle est disponible à cette adresse : https://tangojuice.herokuapp.com/



### Dépendances et Librairies

[Spacy](https://spacy.io) se charge de la lemmatization, de la tokenisation et de l’étiquetage morphosyntaxique. Nous utilisons. Nous utilisons 5 modèles (anglais, français, allemand, japonais, chinois).

[FastApi]() gère tout le backend de l’application. 

##### APIs utilisées

[DeepL](https://pypi.org/project/deepl/) pour la traduction automatique.

[Youtube Transcript API](https://pypi.org/project/youtube-transcript-api/) permet de  récupérer les sous-titres de vidéos si le nom de domaine est 	 youtube.com.





## Améliorations possibles
*  La sélection des mots proposés pourraient sûrement être rendue plus pertinente avec une approche statistique plus sophistiquée, et en incluant des groupes de plusieurs tokens (par exemple "New York").
*  La traduction est souvent insatisfaisante : on aurait aimé proposer plusieurs traductions, ou en choisir une en fonction du contexte, mais les limites des APIs utilisées ne nous ont pas permis de le faire : la limite de caractères ne nous permettait pas de traduire le texte entier sans payer, et l'API Deepl ne propose qu'une seule traduction.
* On aurait aimé proposer la possibilité de sélectionner, sur la page de résultats, les mots à extraire en flashcards Anki. Cela pourrait être fait en Javascript et nous pensons qu'il faudrait pour cela créer une base de données. En effet, actuellement, nous ne pouvons récupérer les données liée à chaque mot depuis la page des résultats, une fois que nous les affichons ils sont "perdus", à moins de les extraire à nouveau, car nous ne les avons pas stockés dans une base de données.  Nous arrivions à faire sélectionner des mots à l’utilisateur, par des checkboxes. Ces mots étaient stockés dans une liste javascript, mais nous ne savions pas comment l’utiliser dans une requête post. 
* Un point d'optimisation : il serait intéressant de garder le modèle SpaCy utilisé en mémoire afin de pouvoir le réutiliser sans devoir le recharger.