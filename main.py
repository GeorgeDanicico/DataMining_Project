import os

from nltk.corpus import stopwords
from openai import OpenAI
from whoosh.analysis import StemmingAnalyzer
from utils.Constants import Constants
from whoosh.fields import Schema, TEXT
from whoosh import index
from whoosh.qparser import QueryParser, OrGroup

# nltk.download('stopwords')  # it must be downloaded only once
stop_words = set(stopwords.words('english'))

all_content = {}


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


def index_documents(documents, ix):
    writer = ix.writer()

    for title, content in documents.items():
        writer.add_document(title=title, content=content)

    writer.commit()
    return ix


def retrieve(index_name, query):
    with index_name.searcher() as searcher:
        results = searcher.search(query, limit=10, reverse=False)
        if results:
            return [res['title'] for res in results]
        else:
            return None, None


def add_documents_to_index(ix):
    for filename in os.listdir(Constants.WIKI_DIRECTORY):
        filename = os.path.join(Constants.WIKI_DIRECTORY, filename)
        content = process_file(filename)
        all_content.update(content)
        ix = index_documents(content, ix)
    return ix


def create_index():
    my_analyzer = StemmingAnalyzer(expression=r"[\w-]+(\.?\w+)*", stoplist=stop_words)
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
    client = OpenAI(api_key=Constants.CHAT_GPT_API_KEY)

    ix = create_index()
    qp = QueryParser("content", schema=ix.schema, group=OrGroup)
    tp = 0
    tp_chat_gpt = 0
    total = 0
    rank_sum = 0

    for key, value in questions.items():
        total += 1
        query = key + " " + value[0]
        q = qp.parse(query)
        response = retrieve(ix, q)
        if response:
            if response[0] == value[1]:
                tp += 1
                tp_chat_gpt += 1
            rank = get_rank(response, value[1])
            if rank != 0:
                rank_sum += 1 / rank
                tp_chat_gpt += get_precision_using_chat_gpt(response, key, value[1], client)

    precision = tp / total
    precision_chat_gpt = tp_chat_gpt / total
    mrr = rank_sum / total

    print("Correct answers = " + str(tp))
    print("Precision at 1 = " + str(precision))
    print("Precision at 1 with ChatGPT = " + str(precision_chat_gpt))
    print("MRR = " + str(mrr))


def get_rank(result, value):
    try:
        return result.index(value) + 1
    except ValueError:
        return 0


def get_precision_using_chat_gpt(result, question, response, chat_gpt_client):
    message = f"for this question: {question} choose only one option without adding additional text:\n"
    for i in range(0, len(result)):
        message += f"{result[i]} \n"
    chat_gpt_response = chat_with_gpt(chat_gpt_client, message)
    if response == chat_gpt_response:
        return 1
    else:
        return 0


def chat_with_gpt(chat_gpt_client, content):
    response = chat_gpt_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": content,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    test_index()
