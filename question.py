import requests
import json


class Question:
    @staticmethod
    def add_question(dict_args, address):
        response = requests.post(address + "/add_question", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]
