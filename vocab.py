"""
Extract complex Word objects from a string
"""
import itertools
import json
import spacy

from scraper import scrape

# les "fréquences relatives" sont calculées par rapport au mot le plus fréquent
# car on n'a pas le nb de tokens du corpus utilisé
# c'est sûrement pas top !

# TODO déterminer seuils !!!
# peuvent varier en fonction des langues
STOPWORD_THRESHOLD = 0.2
RARE_WORD_THRESHOLD = 0.1e-2

OPEN_CLASS_WORDS = ["ADJ", "ADV", "INTJ", "NOUN", "PROPN", "VERB"]

MODELS = {
    "de": "de_core_news_sm",  # "de_dep_news_trf",
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "ja": "ja_core_news_sm",
    "no": "nb_core_news_sm",
    "zh": "zh_core_web_sm",
}


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

    def add_occurrence(self, sentence):
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
    def __init__(self, lang_frequencies):
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

        return sorted(word_list, key=lambda word: word.doc_freq, reverse=True)[
            :nb_words
        ]


def make_vocab(text, lang):
    print(f"Load {lang} frequency list")
    lang_frequencies = json.load(open(f"frequency_lists/{lang}_full.json", "r"))
    vocab = Vocabulary(lang_frequencies)

    print(f"Load {MODELS[lang]} SpaCy model")
    nlp = spacy.load(MODELS[lang])
    print("Parse text")
    doc = nlp(text)
    print("Extract vocabulary")
    for sent in doc.sents:
        vocab.process_sentence(sent)

    return vocab


if __name__ == "__main__":
    LANG = "de"
    text = scrape(
        "https://www.tagesschau.de/inland/ampelparteien-reaktionen-101.html",
        lang=LANG,
    )
    vocab = make_vocab(text, lang=LANG)
    selected_vocab = vocab.extract_vocab(nb_words=20, onlyRareWords=False)
    for word in selected_vocab:
        print(word)

    # FIXME le sentencizer ça marche pas du tout sur les textes bruts...
