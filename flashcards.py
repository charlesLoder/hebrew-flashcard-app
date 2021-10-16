from collections import Counter
import importlib
import csv
heb_vocab = importlib.import_module("hebrew-vocab-tools")
TokenType, ChunkType, get_tokens_by_chunk, get_tokens = heb_vocab.TokenType, heb_vocab.ChunkType, heb_vocab.get_tokens_by_chunk, heb_vocab.get_tokens
HEBLEX = heb_vocab.heb_lex_tools.HEBLEX

# https://github.com/openscriptures/HebrewLexicon/blob/master/HebrewLexicon.pdf

GLOSSER = HEBLEX()
HEB_LEMMAS_COUNT = Counter(get_tokens(TokenType.lemma))
HEB_LEMMAS_MORPH = dict((y, x)
                        for x, y in get_tokens(TokenType.morph_lemma))


def get_gloss(strongs):
    """return a gloss and morph code, unless is a proper noun"""
    morph_code = HEB_LEMMAS_MORPH[strongs]
    # is it a personal name?
    if morph_code.find('Np') != -1:
        return "Proper Noun"
    gloss = GLOSSER.strongs_to_gloss(strongs)
    # if no gloss, return morph code
    if not gloss:
        return morph_code
    return f"{gloss} ({morph_code})"


def create_csv(book_id, less_than_count=100):
    """
    Create csv files containing lemmas used less than X number of times in a book
    """
    book_counts = Counter(get_tokens_by_chunk(
        TokenType.lemma, ChunkType.book)[book_id])
    f = open(f"{book_id}_{less_than_count}_cards.csv", 'w', encoding="UTF-8")
    writer = csv.writer(f)
    writer.writerow(["Lemma", "Gloss"])
    writer.writerow(["Example (Occurrences)", "Gloss (Parsing)"])
    for (strongs, count) in book_counts.most_common():
        total_count = HEB_LEMMAS_COUNT[strongs]
        if total_count <= less_than_count:
            lemma = f"{GLOSSER.strongs_to_lemma(strongs)} ({str(total_count)}x)"
            gloss = get_gloss(strongs)
            writer.writerow([lemma, gloss])
    f.close()
    return f
