import requests
import json


class Package:
    def activate(self, dict_args, address):
        response = requests.post(address + "/package/activate", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def save(self, dict_args, address):
        response = requests.post(address + "/package/save", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def add_question(self, dict_args, address):
        response = requests.post(address + "/package/add_question", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]
