import re
import os
from whoosh.analysis import StemmingAnalyzer


def process_file(filename, content):
    with open(filename, 'r') as file:
        current_title = None
        analyzer = StemmingAnalyzer()

        for line in file:
            if line.startswith("[[") and line.endswith("]]\n"):
                current_title = line[2:-3]
                content[current_title] = []
            elif current_title and not re.match(r'^=.*=$', line.strip()):
                words = re.findall(r'\b\w+\b', line)
                for word in words:
                    tokens = [token.text for token in analyzer(word, remove_stopwords=True)]
                    if len(tokens) > 0:
                        word = tokens[0]
                        if word and not any(char.isdigit() for char in word):
                            content[current_title].append(word)
                numbers = re.findall(r'\b\d+\b', line)
                content[current_title].extend(numbers)
    return content


# TODO - change directory path to your own
dirname = 'directory_path'
dictionary = {}
for filename in os.listdir(dirname):
    filename = os.path.join(dirname, filename)
    content = process_file(filename, dictionary)
    print(content)
