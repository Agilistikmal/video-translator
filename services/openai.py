from openai import OpenAI


class OpenAIService:
    def __init__(self):
        self.client: OpenAI = None
        self.model: str = None

    @classmethod
    def deepseek_client(cls, api_key: str):
        instance = cls()
        instance.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        instance.model = "deepseek-chat"
        return instance

    def send_message(self, message: str, response_with_json: bool = False):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": message}],
            response_format={"type": "json_object"} if response_with_json else None,
        )
        return response.choices[0].message.content
