# Projet interface web

[Consignes](https://loicgrobol.github.io/web-interfaces/assignments/projets.html)

## Objectifs du projet

Créer une application web qui extrait du vocabulaire d'un site web, texte ou fichier de sous-titre afin de permettre le pré-apprentissage du vocabulaire à des apprenants de niveau intermédiaire ou avancé.

## Données

[Listes de fréquences](https://github.com/hermitdave/FrequencyWords) calculées à partir du corpus OpenSubtitles

## Méthodologie

### Répartition du travail

Nous avons réalisé des points hebdomadaires lors desquels nous avons présenté notre avancement l'un à l'autre et intégré les nouveautés dans le code. Le code était partagé via un dossier sur GitHub. Nous tenions à jour une liste des tâches à réaliser dans un fichier .markdown dans notre dossier GitHub.

### Identification des problèmes
- Comment sélectionner les mots à extraire ?
- Comment accélérer le traitement du vocabulaire ? > charger les modèles spacy en amont, pas à chaque extraction ? > memory exceeded sur Heroku :(. Créer différentes pages pour chaque langue dispo, charger juste les ressources pour la langue qu'on veut...

### Etapes du projet

Nous avons commencé par réaliser des versions initiales de l'algorithme d'extraction du vocabulaire, et de l'API qui permet d'interagir avec cet algorithme. Nous avons également commencé à développer l'interface visuelle dès le début du projet. Cet aller-retour permanent entre interface utilisateur et algorithme nous a permis de mieux comprendre quelles fonctionnalités seraient utiles à l'utilisateur.rice.

Nous avons ensuite progressivement amélioré ces trois volets de notre projet afin d'améliorer nos résultats et leur présentation.

## Implémentation

Modèle / Vue / Controlleur ?

Utilisation des API

Hébergement sur Heroku

## Résultats

Prendre des exemples de sites / textes / sous-titres et analyser les résultats

## Discussion

