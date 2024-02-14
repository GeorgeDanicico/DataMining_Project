import nltk
from nltk.corpus import stopwords
from whoosh.analysis import Filter
import spacy

nltk.download('stopwords')  # it must be downloaded only once

class CustomFilter(Filter):
    def __init__(self):
        self.__stop_words = set(stopwords.words('english'))
        self.__nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def __call__(self, tokens):
        def __call__(self, tokens):
            for token in tokens:
                doc = self.__nlp(token.text)
                token.text = doc[0].lemma_
                yield token
