from nltk.stem import WordNetLemmatizer
from whoosh.analysis import CompositeAnalyzer


class Lemmatizer:
    def __init__(self):
        self.__lemmatizer = WordNetLemmatizer()

    def lemmatize(self, token):
        return self.__lemmatizer.lemmatize(token)

    def process(self, tokens):
        return [self.lemmatize(token) for token in tokens]

    def __or__(self, other):
        return CompositeAnalyzer(self, other)

    @staticmethod
    def composable(fn):
        def wrapper(*args, **kwargs):
            result = fn(*args, **kwargs)
            if isinstance(result, list):
                return Lemmatizer().process(result)
            return result

        return wrapper
