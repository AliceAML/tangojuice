"""
Extract complex Word objects from a string
"""
import itertools
import json
import spacy
from collections import defaultdict

from scraper import scrape
from deepl_translate import translate


STOPWORD_THRESHOLD = 1

# seuil par défaut, si pas de définition pour une langue
RARE_WORD_THRESHOLD = defaultdict(lambda: 0.0001)
# TODO déterminer seuils par langue en regardant les listes de fréquence
# RARE_WORD_THRESHOLD["de"] = 0.0005
RARE_WORD_THRESHOLD["fr"] = 0.00016
# peuvent varier en fonction des langues

OPEN_CLASS_WORDS = ["ADJ", "ADV", "INTJ", "NOUN", "PROPN", "VERB"]

MODEL_NAMES = {
    "de": "de_core_news_sm",
    "en": "en_core_web_sm",
    "fr": "fr_core_news_sm",
    "ja": "ja_core_news_sm",
    "no": "nb_core_news_sm",
    "zh": "zh_core_web_sm",
}


def is_not_alpha(word: str):
    return all(not c.isalpha() for c in word)


class Word:
    """
    A Word object represents a LEXEME with its POS, frequencies
    and sentences where it occurs.
    """

    newid = itertools.count()  # count nb of word objects

    def __init__(self, lemme, forme, pos, lang_frequencies: dict, lang):
        self.id = next(Word.newid)
        self.lemme = lemme
        self.forms = {forme}
        self.pos = pos
        self.occurrences = []
        self.lang_freq = float(lang_frequencies.get(lemme, 0))
        self.doc_freq = 0
        self.translation = ""
        self.lang = lang

    def add_occurrence(self, forme, sentence: str):
        """
        Add an occurrence to the word.
        """
        self.forms.add(forme)
        self.occurrences.append(sentence)
        self.doc_freq += 1

    def is_rare(self) -> bool:
        """
        Return true if this word is rare
        """
        return self.lang_freq < RARE_WORD_THRESHOLD[self.lang]

    def __str__(self):
        return f"{self.id:<4} {self.lemme:<15} {self.pos:<5} {self.doc_freq:<2} {self.lang_freq:.10f}"  # {self.occurrences}"


class Vocabulary:
    """
    Object that contains a list of Word objects.
    """

    def __init__(self, input_lang, output_lang, lang_frequencies: dict):
        self.lang_frequencies = lang_frequencies
        self.words = {}
        self.input_lang = input_lang
        self.output_lang = output_lang

    def __iter__(self):
        for word in self.words.values():
            yield word

    def add_word(self, word):
        self.words[word.lemme] = word

    def process_sentence(self, sentence):
        """
        Add tokens from this sentence to the vocabulary.
        """
        for word in sentence:
            key = word.lemma_ + word.pos_
            # do not include stopwords and punctuation
            if (
                self.lang_frequencies.get(word.lemma_, 0) > STOPWORD_THRESHOLD
                or word.pos_ not in OPEN_CLASS_WORDS  # rejeter toutes les POS fermées
                or is_not_alpha(word.text)
            ):
                continue
            elif key in self.words:
                self.words[key].add_occurrence(forme=word.text, sentence=sentence.text)
            else:
                self.words[key] = Word(
                    word.lemma_,
                    word.norm_,
                    word.pos_,
                    self.lang_frequencies,
                    self.input_lang,
                )
                self.words[key].add_occurrence(word.norm_, sentence.text)

    def __str__(self) -> str:
        return "\n".join(str(word) for word in self.words.values() if word.doc_freq > 1)

    def extract_vocab(self, nb_words=None, onlyRareWords: bool = False) -> list[Word]:
        """
        Return a list of nb_words most frequent words.
        """
        if nb_words is None:
            nb_words = len(self.words)  # default value = return all the words
        print(f"Select {nb_words} most common words in the document.")

        if onlyRareWords:
            print(
                f"Only keep words with a frequency < {RARE_WORD_THRESHOLD[self.input_lang]}"
            )
            word_list = (word for word in self.words.values() if word.is_rare())
        else:
            word_list = self.words.values()
        # tri par fréquence relative lang (ascendant)
        word_list = sorted(word_list, key=lambda word: word.lang_freq, reverse=False)
        # tri par fréquence doc (descendant)
        word_list = sorted(word_list, key=lambda word: word.doc_freq, reverse=True)
        word_list = word_list[:nb_words]

        print(f"Translating {nb_words} words...")
        for word in word_list:
            try:
                word.translation = translate(
                    word.lemme, src=self.input_lang, dest=self.output_lang
                )
            except Exception as e:
                print("Could not translate word")
        return word_list


def make_vocab(text, input_lang, output_lang):
    # normalize apostrophes in text, to prevent tokenization issues
    text = text.replace("’", "'")

    print(f"Load {input_lang} frequency list")
    lang_frequencies = json.load(
        open(f"frequency_lists/{input_lang}_full_lemmas.json", "r")
    )
    vocab = Vocabulary(input_lang, output_lang, lang_frequencies)

    print(f"Load {MODEL_NAMES[input_lang]} SpaCy model")
    nlp = spacy.load(MODEL_NAMES[input_lang])

    print("Parse text")
    doc = nlp(text)
    print("Extract vocabulary")
    for sent in doc.sents:
        vocab.process_sentence(sent)

    print(f"{len(vocab.words)} lexemes extracted")
    return vocab


if __name__ == "__main__":  # tests
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
    vocab = make_vocab(text, input_lang=LANG, output_lang="FR")
    selected_vocab = vocab.extract_vocab(nb_words=20, onlyRareWords=True)
    for word in selected_vocab:
        print(word)
