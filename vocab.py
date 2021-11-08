"""
Extract complex Word objects from a string
"""
import itertools
import json
import spacy

from scraper import scrape

MODELS = {
    "de": "de_core_news_sm",
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
        self.lang_freq = lang_frequencies[
            lemme
        ]  # FIXME c'est un problème de prendre seulement la fréquence du lemme...
        self.doc_freq = 0

    def add_occurrence(self, sentence):
        """
        Add an occurrence to the word.
        """
        self.occurrences.append(sentence)
        self.doc_freq += 1

    def is_rare() -> bool:
        """
        Return true if this word is rare
        """
        return False  # TODO déterminer un seuil...

    def __str__(self):
        return f"{self.id} {self.lemme.upper()} {self.pos} {self.doc_freq} {self.lang_freq}"


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
        for word in sentence:
            # do not include stopwords  > TODO déterminer seuil !!!
            if self.lang_frequencies.get(word.lemma_, 1) > 0.05:
                continue
            elif word.lemma_ in self.words:
                self.words[word.lemma_].add_occurrence(sentence)
            else:
                self.words[word.lemma_] = Word(
                    word.lemma_, word.pos_, self.lang_frequencies
                )
                self.words[word.lemma_].add_occurrence(sentence)

    def __str__(self) -> str:
        return "\n".join(str(word) for word in self.words.values() if word.doc_freq > 1)

    def select_vocab(self, nb_words=None, includeCommonWords: bool = True):
        """
        Return a list of nb_words most frequent words.
        """
        print(f"Select {nb_words} most common words in the document.")
        if nb_words is None:
            nb_words = len(self.words)  # default value = return all the words

        if includeCommonWords:
            return sorted(
                self.words.values(), key=lambda word: word.doc_freq, reverse=True
            )[:nb_words]
        else:
            return sorted(
                (word for word in self.words.values() if word.is_rare()),
                key=lambda word: word.doc_freq,
                reverse=True,
            )[:nb_words]


def make_vocab(text, lang):
    print(f"Load {lang} frequency list")
    lang_frequencies = json.load(open(f"frequency_lists/{lang}_full.json", "r"))
    vocab = Vocabulary(lang_frequencies)

    print(f"Load {lang} SpaCy model")
    nlp = spacy.load(MODELS[lang])
    print("Parse text")
    doc = nlp(text)
    print("Extract vocabulary")
    for sent in doc.sents:
        vocab.process_sentence(sent)

    return vocab


if __name__ == "__main__":
    LANG = "fr"
    text = scrape(
        "https://u-paris.fr/linguistique/procedure-pour-effectuer-un-stage/",
        lang=LANG,
    )
    vocab = make_vocab(text, lang=LANG)
    selected_vocab = vocab.select_vocab(nb_words=20)
    for word in selected_vocab:
        print(word)

    # FIXME le sentencizer ça marche pas du tout sur les textes bruts...
