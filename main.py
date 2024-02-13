import os

from nltk.corpus import stopwords
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
from lemmatizer import LemmatizationFilter
from utils.Constants import Constants
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
            if line.startswith("[[") and line.endswith("]]\n"):
                if current_title:
                    content[current_title] = body
                    body = ""
                current_title = line[2:-3]
            elif current_title and line.strip():
                processed_line = process_line(line.strip())
                body += " " + processed_line

    print(filename)
    return content


def process_line(line):
    if line.startswith("==") and line.endswith("=="):
        num_eq = line.lstrip('=').count('=')
        processed_line = line[num_eq:-num_eq]
    elif line.startswith(Constants.REDIRECT_PREFIX):
        processed_line = line[10:]
    elif Constants.HTTP_PREFIX in line:
        processed_line = line.replace(Constants.HTTP_PREFIX, "")
    elif Constants.HTTPS_PREFIX in line:
        processed_line = line.replace(Constants.HTTPS_PREFIX, "")
    else:
        processed_line = line

    return processed_line


def index_documents(content, ix):
    writer = ix.writer(procs=4, multisegment=True)

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


def create_index():
    my_analyzer = RegexTokenizer(expression=r"[\w-]+(\.?\w+)*") | LowercaseFilter() | LemmatizationFilter() | StopFilter(stop_words)
    schema = Schema(title=TEXT(stored=True, analyzer=my_analyzer, field_boost=2.0), content=TEXT(analyzer=my_analyzer))

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
    q = qp.parse(
        u"Daniel Hertzberg & James B. Stewart of this paper shared a 1988 Pulitzer for their stories about insider trading")
    result = retrieve(ix, q)

    print(f"The most similar Wikipedia page is: {result}")


def load_questions(filename):
    questions = {}

    with open(filename, 'r', errors='ignore') as file:
        line_index = 0
        for line in file:
            if not line.strip():
                continue
            striped_line = line.strip()
            if line_index == 0:
                category = striped_line
                line_index += 1
            elif line_index == 1:
                question = striped_line
                line_index += 1
            elif line_index == 2:
                questions[question] = [category, striped_line]
                line_index = 0
    return questions


def test_index():
    questions = load_questions("questions.txt")


if __name__ == "__main__":
    start()
    test_index()
