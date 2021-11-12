"""
Extract complex Word objects from a string
"""
import itertools
import json
import spacy
from string import punctuation

from scraper import scrape

# les "fréquences relatives" sont calculées par rapport au mot le plus fréquent
# car on n'a pas le nb de tokens du corpus utilisé
# c'est sûrement pas top !

# TODO déterminer seuils !!!
# peuvent varier en fonction des langues
STOPWORD_THRESHOLD = 1
RARE_WORD_THRESHOLD = 0.1e-2

OPEN_CLASS_WORDS = ["ADJ", "ADV", "INTJ", "NOUN", "PROPN", "VERB"]

# LOAD RESSOURCES EVERYTIME THE APP IS STARTED
MODEL_NAMES = {
    "de": "de_core_news_sm",  # "de_dep_news_trf",
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "ja": "ja_core_news_sm",
    "no": "nb_core_news_sm",
    "zh": "zh_core_web_sm",
}

SPACY_MODELS = {}
LANG_FREQUENCIES = {}
for i, (lang, model) in enumerate(MODEL_NAMES.items()):
    print(f"Load {model} SpaCy model ({i+1}/{len(MODEL_NAMES)})")
    try:
        SPACY_MODELS[lang] = spacy.load(model)
    except Exception as e:
        print(f"Could not load {model} model")
        print(e)
    print(f"Load {lang} frequency list")
    try:
        LANG_FREQUENCIES[lang] = json.load(
            open(f"frequency_lists/{lang}_full.json", "r")
        )
    except Exception as e:
        print(f"Could not load {lang} frequency list")
        print(e)


def is_punct(word: str):
    return all(c in punctuation for c in word)


class Word:
    """
    A Word object represents a LEXEME with its POS, frequencies
    and sentences where it occurs.
    """

    newid = itertools.count()  # count nb of word objects

    def __init__(self, lemme, pos, lang_frequencies: dict):
        self.id = next(Word.newid)
        self.lemme = lemme
        self.pos = pos
        self.occurrences = []
        self.lang_freq = lang_frequencies.get(lemme, 0)
        # FIXME c'est un problème de prendre seulement la fréquence du lemme...
        self.doc_freq = 0

    def add_occurrence(self, sentence: str):
        """
        Add an occurrence to the word.
        """
        self.occurrences.append(sentence)
        self.doc_freq += 1

    def is_rare(self) -> bool:
        """
        Return true if this word is rare
        """
        return self.lang_freq < RARE_WORD_THRESHOLD

    def __str__(self):
        return f"{self.id:<4} {self.lemme:<15} {self.pos:<5} {self.doc_freq:<2} {self.lang_freq:.10f}"  # {self.occurrences}"


class Vocabulary:
    def __init__(self, lang_frequencies: dict):
        self.lang_frequencies = lang_frequencies
        self.words = {}

    def add_word(self, word):
        self.words[word.lemme] = word

    def process_sentence(self, sentence):
        """
        Add tokens in the sentence to the vocabulary.
        """
        # print(sentence)
        for word in sentence:
            key = word.lemma_ + word.pos_
            # print(key)
            # do not include stopwords and punctuation
            if (
                self.lang_frequencies.get(word.lemma_, 0) > STOPWORD_THRESHOLD
                # or not word.is_alpha
                # TODO rejecter toutes les POS fermées ?
                or word.pos_ not in OPEN_CLASS_WORDS
                # complete list : https://universaldependencies.org/u/pos/
                or is_punct(word.text)
            ):
                continue
            elif key in self.words:
                self.words[key].add_occurrence(sentence.text)
            else:
                self.words[key] = Word(word.lemma_, word.pos_, self.lang_frequencies)
                self.words[key].add_occurrence(sentence.text)

    def __str__(self) -> str:
        return "\n".join(str(word) for word in self.words.values() if word.doc_freq > 1)

    def extract_vocab(self, nb_words=None, onlyRareWords: bool = False):
        """
        Return a list of nb_words most frequent words.
        """
        print(f"Select {nb_words} most common words in the document.")
        if nb_words is None:
            nb_words = len(self.words)  # default value = return all the words

        if onlyRareWords:
            word_list = (word for word in self.words.values() if word.is_rare())
        else:
            word_list = self.words.values()
        # ajouter un premier tri par inverse de lang_freq ?

        word_list = sorted(word_list, key=lambda word: word.lang_freq, reverse=False)

        return sorted(word_list, key=lambda word: word.doc_freq, reverse=True)[
            :nb_words
        ]


def make_vocab(text, lang):
    # normalize apostrophes in text
    text = text.replace("’", "'")

    lang_frequencies = LANG_FREQUENCIES[lang]
    nlp = SPACY_MODELS[lang]

    vocab = Vocabulary(lang_frequencies)

    print("Parse text")
    doc = nlp(text)
    print("Extract vocabulary")
    for sent in doc.sents:
        vocab.process_sentence(sent)

    print(f"{len(vocab.words)} lexemes extracted")
    return vocab


if __name__ == "__main__":
    LANG = "en"
    # text = scrape(
    #     "https://www.leparisien.fr/faits-divers/mayenne-une-joggeuse-de-17-ans-portee-disparue-un-dispositif-de-recherches-lance-08-11-2021-Z6EITYD6OFE23I2S2BR3RP2YOA.php",
    #     lang=LANG,
    # )
    text = """
    Hey folks,
One of our long term roommates is unfortunately leaving Berlin 💔, so a room & his furniture will become available from January 2nd. It is a spacious 32m room in a 2 storey WG with 4 other roommates; Jonathan (Myself), Emma, Steph & Antoinette - we live in a calm and relaxed environment so if you're looking for a party place this isn't for you. We work and study between home and studios/offices in a variety of tech and creative fields - so if you need to home office too, there's plenty of space!  Ideally looking a queer man as his replacement to keep a balance in the apartment. (No couples or pets🤧)
The price of the room is 650€/month(All utilities included) with 1 month deposit and a furniture takeover fee of 300€ (This includes a large double bed, pillows, duvet, sofa bed, cushions, coffee table, wardrobe, 3 side tables, lamps) with an optional new Samsung TV and stand for 400€. 
(Pictures of this can be provided separately- the furniture is not the one in the pictures)
Please send a DM with some info about yourself. We will be arranging either in-person meetings or video calls in the coming days.
    """
    vocab = make_vocab(text, lang=LANG)
    selected_vocab = vocab.extract_vocab(nb_words=20, onlyRareWords=False)
    for word in selected_vocab:
        print(word)

    # FIXME le sentencizer ça marche pas du tout sur les textes bruts...
    # FIXME certaines expressions ne devraient pas être tokenisées, comme "New York" (surtout les entités nommées)
    # FIXME problème de scraping, parfois on chope encore des bouts de code HTML inutiles
    # ex : "Pfeil runter" sur "https://www.tagesschau.de/ausland/amerika/usa-reisende-101.html"
