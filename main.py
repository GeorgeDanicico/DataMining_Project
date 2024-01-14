import re
import os

import nltk
from nltk.corpus import stopwords
from whoosh.analysis import StemmingAnalyzer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def process_file(filename, content):
    with open(filename, 'r') as file:
        current_title = None

        for line in file:
            if line.startswith("[[") and line.endswith("]]\n"):
                current_title = line[2:-3]
                content[current_title] = set()
            elif current_title and not re.match(r'^=.*=$', line.strip()):
                words = re.findall(r'\b\w+\b', line)
                for word in words:
                    if word not in stop_words:
                        if not any(char.isdigit() for char in word):
                            content[current_title].add(word.lower())
                numbers = set(re.findall(r'\b\d+\b', line))
                content[current_title].update(numbers)
    return content


# TODO - change directory path to your own
dirname = '/Users/george/Downloads/wiki'
dictionary = {}
for filename in os.listdir(dirname):
    filename = os.path.join(dirname, filename)
    content = process_file(filename, dictionary)
    print(content)
    break
