from whoosh.analysis import Filter
import spacy


class LemmatizationFilter(Filter):
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

    def __call__(self, tokens):
        for token in tokens:
            doc = self.__nlp(token.text)
            token.text = doc[0].lemma_
            yield token
