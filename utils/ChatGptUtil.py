from openai import OpenAI

from utils.Constants import Constants


class ChatGptUtil:
    def __init__(self):
        self.__client = OpenAI(api_key=Constants.CHAT_GPT_API_KEY)

    def chat_with_gpt(self, user_content):
        response = self.__client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_content,
                }
            ],
            model="gpt-3.5-turbo",
        )
        return response.choices[0].message.content
