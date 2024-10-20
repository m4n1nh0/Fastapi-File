import requests

from settings.config import Config


class APIClient:
    def __init__(self):
        self.api_url = Config.FLASK_API_URL

    def send_data(self, data):
        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao enviar dados: {e}")
