import re
import os
from nltk.corpus import stopwords
from whoosh.fields import Schema, TEXT
from whoosh.lang.porter import stem
from whoosh import index, scoring
from whoosh.qparser import QueryParser

# nltk.download('stopwords')  # it must be downloaded only once
stop_words = set(stopwords.words('english'))

def process_file(filename, content):
    with open(filename, 'r', errors='ignore') as file:
        current_title = None

        for line in file:
            print(line)
            if line.startswith("[[") and line.endswith("]]\n"):
                current_title = line[2:-3]
                content[current_title] = set()
            elif current_title and not re.match(r'^=.*=$', line.strip()):
                words = re.findall(r'\b\w+\b', line)
                for word in words:
                    if word not in stop_words:
                        if not any(char.isdigit() for char in word):
                            content[current_title].add(stem(word.lower()))
                numbers = set(re.findall(r'\b\d+\b', line))
                content[current_title].update(numbers)
    return content

def index_documents(stemmed_content, ix):
    writer = ix.writer()

    for current_title in stemmed_content:
        current_content = ' '.join(stemmed_content[current_title])
        writer.add_document(title=current_title, content=current_content)

    writer.commit()

    return ix


def retrieve(index_name, query):
    with index_name.searcher(weighting=scoring.TF_IDF()) as searcher:

        results = searcher.search(query, limit=None)
        if results:
            return results[0]['title']
        else:
            return None


def start():

    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))

    if not os.path.exists("my_index_directory"):
        os.mkdir("my_index_directory")

    ix = index.create_in("my_index_directory", schema)

    # TODO - change directory path to your own
    dirname = '../FileExample/'
    dictionary = {}

    for filename in os.listdir(dirname):
        filename = os.path.join(dirname, filename)
        content = process_file(filename, dictionary)
        ix = index_documents(content, ix)


    qp = QueryParser("content", schema=ix.schema)
    q = qp.parse(u"r redirect tpl")
    result = retrieve(ix, q)

    print(f"The most similar Wikipedia page is: {result}")


start()