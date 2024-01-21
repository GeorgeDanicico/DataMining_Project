from whoosh.analysis import Filter, RegexTokenizer
import spacy


class LemmatizationFilter(Filter):
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_sm")

    def __call__(self, tokens):
        for token in tokens:
            doc = self.__nlp(token.text)
            token.text = doc[0].lemma_
            yield token


if __name__ == "__main__":
    tokenizer = RegexTokenizer(r"[\w-]+(\.?\w+)*")
    for token in tokenizer(u"|title=Kitemark.com      |publisher=Kitemark.com |date= |accessdate=2012-04-03[/tpl]"):
        print(token.text)
