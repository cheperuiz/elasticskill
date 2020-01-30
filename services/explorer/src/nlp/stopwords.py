# pylint: disable=import-error
# pylint: disable=no-name-in-module

import os
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from utils.string import clean_string

EXTRA_STOPWORDS_PATH = os.environ["PROJECT_SRC"] + "/nlp/stop_words.txt"


def extra_stopwords(stop_words_path=EXTRA_STOPWORDS_PATH):
    try:
        with open(stop_words_path) as f:
            sw = f.read().split("\n")
        return sw
    except:
        return set()


def get_stopwords(default_stopwords=set(stopwords.words("english")), extra_stopwords=extra_stopwords()):
    sw = default_stopwords.union(extra_stopwords)
    return sw


def is_valid_term(term, stop_words=get_stopwords()):
    if term in stop_words or term in ["https"]:
        return False
    if term.replace(".", "").replace("x", "").replace(":", "").isnumeric():
        return False
    if term.startswith("0x"):
        return False
    return True


def remove_stopwords(text, stop_words=get_stopwords(), remove_numbers=False):
    if type(text) is bytes:
        text = text.decode("utf-8")
    text = clean_string(text)
    words = word_tokenize(text)
    words = [word for word in words if word.lower() not in stop_words]
    if remove_numbers:
        words = [
            word for word in words if not word.replace(".", "").replace(":", "").replace("x", "").isnumeric()
        ]
    return " ".join(words)
