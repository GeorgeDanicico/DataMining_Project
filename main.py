import nltk
from nltk.corpus import stopwords

from IndexTest import IndexTest
from utils.Constants import Constants

if __name__ == "__main__":
    # nltk.download('stopwords')  # it must be downloaded only once
    stop_words = set(stopwords.words('english'))
    index_test = IndexTest(Constants.WIKI_DIRECTORY, stop_words)
    index_test.test_index()
