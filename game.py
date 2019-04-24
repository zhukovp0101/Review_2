import requests
import json


class Game:
    def activate(self, dict_args, address):
        response = requests.post(address + "/game/activate", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def show_table(self, dict_args, address):
        response = requests.get(address + "/game/show_table", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        participants = dict_response["participants"]
        for name, points in participants.items():
            print("{0} has {1} points".format(name, points))
        return dict_response["result_info"]

    def add_participant(self, dict_args, address):
        response = requests.post(address + "/game/add_participant", json=dict_args) # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def add_points(self, dict_args, address):
        response = requests.post(address + "/game/add_points", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def get_question(self, dict_args, address):
        response = requests.get(address + "/game/get_question", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        print(dict_response["question"])
        return dict_response["result_info"]

    def get_answer(self, dict_args, address):
        response = requests.get(address + "/game/get_answer", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        print(dict_response["answer"])
        return dict_response["result_info"]

    def save(self, dict_args, address):
        response = requests.post(address + "/game/save", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    def load_previous(self, dict_args, address):
        response = requests.post(address + "/game/load_previous", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]
