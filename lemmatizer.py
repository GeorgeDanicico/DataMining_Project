from whoosh.analysis import Filter
import spacy


class LemmatizationFilter(Filter):
    def __init__(self):
        self.__nlp = spacy.load("en_core_web_sm")

    def __call__(self, tokens):
        batch_size = 1000
        texts = [token.text for token in tokens]

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_docs = self.__nlp.pipe(batch_texts, disable=["parser", "ner"])

            for doc in batch_docs:
                for token, token_doc in zip(tokens, doc):
                    token.text = token_doc.lemma_
                    yield token
