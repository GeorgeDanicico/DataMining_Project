import os

from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import Schema, TEXT

from utils.Constants import Constants


class Index:
    def __init__(self, filename, stop_words):
        self.__ix = None
        self.__filename = filename
        self.__stop_words = stop_words
        self.__create_index()

    def __create_index(self):
        self.__stop_words.add(Constants.TPL_TAG)
        self.__stop_words.add(Constants.REF_TAG)
        my_analyzer = StemmingAnalyzer(expression=r"[\w-]+(\.?\w+)*", stoplist=self.__stop_words)
        schema = Schema(title=TEXT(stored=True, analyzer=my_analyzer, field_boost=2.0),
                        content=TEXT(analyzer=my_analyzer))

        if not os.path.exists(Constants.INDEX_DIRECTORY):
            os.mkdir(Constants.INDEX_DIRECTORY)
            self.__ix = index.create_in(Constants.INDEX_DIRECTORY, schema)
            directory_exists = False
        else:
            self.__ix = index.open_dir(Constants.INDEX_DIRECTORY)
            directory_exists = True

        if not directory_exists:
            self.__add_documents_to_index()

    def __add_documents_to_index(self):
        for filename in os.listdir(Constants.WIKI_DIRECTORY):
            filename = os.path.join(Constants.WIKI_DIRECTORY, filename)
            content = self.__process_file(filename)
            self.__index_documents(content)

    def __process_file(self, filename):
        content = {}
        with open(filename, 'r', errors='ignore') as file:
            current_title = None
            body = ""

            for line in file:
                if line.startswith("[[") and not line.startswith(Constants.IMAGE_TAG) \
                        and not line.startswith(Constants.FILE_TAG) \
                        and line.endswith("]]\n"):
                    if current_title:
                        content[current_title] = body
                        body = ""
                    current_title = line[2:-3]
                elif current_title and line.strip():
                    processed_line = self.__process_line(line.strip())
                    body += " " + processed_line

        print(filename)
        return content

    def __index_documents(self, documents):
        writer = self.__ix.writer()

        for title, content in documents.items():
            writer.add_document(title=title, content=content)

        writer.commit()

    def get_index(self):
        return self.__ix

    def retrieve(self, query):
        with self.__ix.searcher() as searcher:
            results = searcher.search(query, limit=None, reverse=False)
            if results:
                return [res['title'] for res in results]
            else:
                return None, None

    @staticmethod
    def __process_line(line):
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



