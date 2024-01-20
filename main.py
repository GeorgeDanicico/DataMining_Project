from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter, Filter, StemmingAnalyzer

from lemmatizer import Lemmatizer
from utils.Constants import Constants
import os
from nltk.corpus import stopwords
from whoosh.fields import Schema, TEXT
from whoosh import index, scoring
from whoosh.qparser import QueryParser

# nltk.download('stopwords')  # it must be downloaded only once
stop_words = set(stopwords.words('english'))


def process_file(filename):
    content = {}

    with open(filename, 'r', errors='ignore') as file:
        current_title = None
        body = ""

        for line in file:
            print(line)

            if line.startswith("[[") and line.endswith("]]\n"):
                if current_title:
                    content[current_title] = body
                    body = ""
                current_title = line[2:-3]
            elif current_title and line.strip():
                body += " " + line.strip()

    return content


def index_documents(content, ix):
    writer = ix.writer()

    for current_title in content:
        writer.add_document(title=current_title, content=content[current_title])

    writer.commit()
    return ix


def retrieve(index_name, query):
    with index_name.searcher(weighting=scoring.TF_IDF()) as searcher:

        results = searcher.search(query, limit=None)
        if results:
            return results[0]['title']
        else:
            return None


def add_documents_to_index(ix):
    for filename in os.listdir(Constants.WIKI_DIRECTORY):
        filename = os.path.join(Constants.WIKI_DIRECTORY, filename)
        content = process_file(filename)
        ix = index_documents(content, ix)
    return ix


def LemmatizationFilter(stream):
    for token in stream:
        yield token


def create_index():
    my_analyzer = StemmingAnalyzer() | StopFilter() | LowercaseFilter()
    schema = Schema(title=TEXT(stored=True, analyzer=my_analyzer), content=TEXT(analyzer=my_analyzer))

    if not os.path.exists(Constants.INDEX_DIRECTORY):
        os.mkdir(Constants.INDEX_DIRECTORY)
        ix = index.create_in(Constants.INDEX_DIRECTORY, schema)
        directory_exists = False
    else:
        ix = index.open_dir(Constants.INDEX_DIRECTORY)
        directory_exists = True

    if not directory_exists:
        ix = add_documents_to_index(ix)

    return ix


def start():
    ix = create_index()

    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(u"Daniel Hertzberg & James B. Stewart of this paper shared a 1988 Pulitzer for their stories about insider trading")
    result = retrieve(ix, q)

    print(f"The most similar Wikipedia page is: {result}")


if __name__ == "__main__":
    start()
