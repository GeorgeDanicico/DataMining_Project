from whoosh.qparser import QueryParser, OrGroup

from Index import Index
from utils.ChatGptUtil import ChatGptUtil
from utils.Constants import Constants


class IndexTest:
    def __init__(self, filename, stop_words):
        self.__stop_words = stop_words
        self.__myIndex = Index(filename, stop_words)
        self.__chatGptUtil = ChatGptUtil()

    def test_index(self):
        questions = self.load_questions(Constants.QUESTIONS_FILE)

        qp = QueryParser("content", schema=self.__myIndex.get_index().schema, group=OrGroup)

        tp = 0
        tp_chat_gpt = 0
        total = 0
        rank_sum = 0

        for key, value in questions.items():
            total += 1
            query = key + " " + value[0]
            q = qp.parse(query)
            response = self.__myIndex.retrieve(q)
            if response:
                if response[0] == value[1]:
                    tp += 1
                    tp_chat_gpt += 1
                rank = self.get_rank(response, value[1])
                if rank != 0:
                    rank_sum += 1 / rank
                    if rank <= 10:
                        tp_chat_gpt += self.__get_precision_using_chat_gpt(response[0:10], key, value[1])

        precision = tp / total
        precision_chat_gpt = tp_chat_gpt / total
        mrr = rank_sum / total

        print("Correct answers = " + str(tp))
        print("Precision at 1 = " + str(precision))
        print("Precision at 1 with ChatGPT = " + str(precision_chat_gpt))
        print("MRR = " + str(mrr))

    @staticmethod
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

    @staticmethod
    def get_rank(result, value):
        try:
            return result.index(value) + 1
        except ValueError:
            return 0

    def __get_precision_using_chat_gpt(self, result, question, response):
        message = f"for this question: {question} choose only one option without adding additional text:\n"
        for i in range(0, len(result)):
            message += f"{result[i]} \n"
        chat_gpt_response = self.__chatGptUtil.chat_with_gpt(message)
        if response == chat_gpt_response:
            return 1
        else:
            return 0