import requests
import json


class Game:
    @staticmethod
    def activate(dict_args, address):
        response = requests.post(address + "/game/activate", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def show_table(dict_args, address):
        response = requests.get(address + "/game/show_table", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        table = dict_response["table"]
        for participant, points in table.items():
            print("{0} has {1} points.".format(participant, points))
        return dict_response["result_info"]

    @staticmethod
    def add_participant(dict_args, address):
        response = requests.post(address + "/game/add_participant", json=dict_args) # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def add_points(dict_args, address):
        response = requests.post(address + "/game/add_points", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def get_question(dict_args, address):
        response = requests.post(address + "/game/get_question", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        if dict_response["result_info"].get("status") == "OK":
            print("Package: {}".format(dict_response["package"]))
            print("Author: {}".format(dict_response["author"]))
            print("Complexity: {}".format(dict_response["complexity"]))
            print("Name: {}".format(dict_response["name"]))
            print("Question: {}".format(dict_response["text"]))
        return dict_response["result_info"]

    @staticmethod
    def get_package(dict_args, address):
        response = requests.post(address + "/game/get_package", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        if dict_response["result_info"].get("status") == "OK":
            print("Author: {}".format(dict_response["author"]))
            print("Name: {}".format(dict_response["name"]))
            print("Complexity: {}".format(dict_response["complexity"]))
        return dict_response["result_info"]

    @staticmethod
    def lost_package(dict_args, address):
        response = requests.post(address + "/game/lost_package", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def get_answer(dict_args, address):
        response = requests.get(address + "/game/get_answer", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        if dict_response["result_info"].get("status") == "OK":
            print(dict_response["answer"])
            print("Comment: {}".format(dict_response["comment"]))
        return dict_response["result_info"]

    @staticmethod
    def save(dict_args, address):
        response = requests.post(address + "/game/save", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]

    @staticmethod
    def load_previous(dict_args, address):
        response = requests.post(address + "/game/load_previous", json=dict_args)  # TODO: server
        dict_response = json.loads(response.text)
        return dict_response["result_info"]
