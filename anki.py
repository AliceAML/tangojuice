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
    INPUT_LANG = "fr"
    OUTPUT_LANG = "en-us"
    # text = scrape(
    #     "https://www.leparisien.fr/faits-divers/mayenne-une-joggeuse-de-17-ans-portee-disparue-un-dispositif-de-recherches-lance-08-11-2021-Z6EITYD6OFE23I2S2BR3RP2YOA.php",
    #     lang=LANG,
    # )
    text = """
    Nous étions à l'Etude, quand le Proviseur entra suivi d'un nouveau habillé en bourgeois et d'un garçon de classe qui portait un grand pupitre. Ceux qui dormaient se réveillèrent, et chacun se leva comme surpris dans son travail.

Le Proviseur nous fit signe de nous rasseoir ; puis, se tournant vers le maître d'études :

- Monsieur Roger, lui dit-il à demi-voix, voici un élève que je vous recommande, il entre en cinquième. Si son travail et sa conduite sont méritoires, il passera dans les grands, où l'appelle son âge.

Resté dans l'angle, derrière la porte, si bien qu'on l'apercevait à peine, le nouveau était un gars de la campagne, d'une quinzaine d'années environ, et plus haut de taille qu'aucun de nous tous. Il avait les cheveux coupés droit sur le front, comme un chantre de village, l'air raisonnable et fort embarrassé. Quoiqu'il ne fût pas large des épaules, son habit-veste de drap vert à boutons noirs devait le gêner aux entournures et laissait voir, par la fente des parements, des poignets rouges habitués à être nus. Ses jambes, en bas bleus, sortaient d'un pantalon jaunâtre très tiré par les bretelles. Il était chaussé de souliers forts, mal cirés, garnis de clous.

On commença la récitation des leçons. Il les écouta de toutes ses oreilles, attentif comme au sermon, n'osant même croiser les cuisses, ni s'appuyer sur le coude, et, à deux heures, quand la cloche sonna, le maître d'études fut obligé de l'avertir, pour qu'il se mît avec nous dans les rangs.

Nous avions l'habitude, en entrant en classe, de jeter nos casquettes par terre, afin d'avoir ensuite nos mains plus libres ; il fallait, dès le seuil de la porte, les lancer sous le banc, de façon à frapper contre la muraille en faisant beaucoup de poussière ; c'était là le genre.
Please send a DM with some info about yourself. We will be arranging either in-person meetings or video calls in the coming days.
    """
    vocab = make_vocab(text, input_lang=INPUT_LANG, output_lang=OUTPUT_LANG)
    selected_vocab = vocab.extract_vocab(nb_words=20, onlyRareWords=False)
    for word in selected_vocab:
        print(word)

    with open("test.apkg", "wb") as f:
        f.write(generate_anki_cards(selected_vocab, "Test").getvalue())
