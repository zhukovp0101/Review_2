import requests
import json


class Package:
    @staticmethod
    def activate(dict_args, address):
        response = requests.post(address + "/package/activate", json=dict_args)
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def save(dict_args, address):
        response = requests.post(address + "/package/save", json=dict_args)
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def add_question(dict_args, address):
        response = requests.post(address + "/package/add_question", json=dict_args)
        dict_response = json.loads(response.text)
        return dict_response["result_info"]
