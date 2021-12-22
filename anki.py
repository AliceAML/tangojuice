"""Generate anki flashcards from our data"""

import genanki
from vocab import Word, Vocabulary, make_vocab
import random
import io

my_model = genanki.Model(
    1,
    "Tango Juice",
    fields=[
        {"name": "Word"},
        {"name": "Example"},
        {"name": "Translation"},
        {"name": "Category"},
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "<h1>{{Word}}</h1>({{Category}})<br><i>{{Example}}</i>",
            "afmt": "{{Translation}}",
        },
    ],
)


def generate_anki_cards(vocab: list[Word], title: str) -> io.BytesIO:
    my_deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), title)

    for word in vocab:
        ex_nb = random.randrange(0, len(word.occurrences))
        example = word.occurrences[ex_nb]
        for form in word.forms:
            example = example.replace(form, "<b>" + form + "</b>")
        my_note = genanki.Note(
            model=my_model,
            fields=[word.lemme, example, word.translation, word.pos],
        )
        my_deck.add_note(my_note)
    stream = io.BytesIO()
    my_deck.write_to_file(stream)
    return stream


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
    vocab = make_vocab(text, input_lang=LANG, output_lang="fr")
    selected_vocab = vocab.extract_vocab(nb_words=20, onlyRareWords=False)
    for word in selected_vocab:
        print(word)

    with open("test.apkg", "wb") as f:
        f.write(generate_anki_cards(selected_vocab, "Test").getvalue())
