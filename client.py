import argparse
import requests
import datetime
import shlex
from sys import stderr
from game import Game
from question import Question
from package import Package


# Эта вещь нужна для того, чтобы вызов справки по командам не вызывал завершение программы.
class ParserException(Exception):
    pass


class NonExitArgumentParser(argparse.ArgumentParser):
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, stderr)
        raise ParserException


# Класс клиента.

class Client:
    def __init__(self):
        self._game = None
        self._game_mode = False  # Включен ли режим игры;
        self._package = None
        self._package_mode = False  # Включен ли режим пакета;
        self._active_now = False  # Является ли клиент активным;
        self._command_line = "> "  # Строка ввода команды;
        self._parsers = self._init_parsers()  # Инициализирует необходимые парсеры для argparse;
        self._set_current_parser(self._parsers["default_parser"]) # Устанавливает парсер по умолчанию (может быть заменен на специальные парсеры режима игры и ввода вопросов для пакета);

    # Устанавливает соединение с сервером.
    def _connect(self, address):
        if address == "":
            print("Enter server address: ", end="")
            address = input()
        valid_address = False
        while not valid_address:
            if address in ["exit"]:
                self._exit()
                return False
            try:
                requests.get(address)
                valid_address = True
            except requests.RequestException:
                print("Enter valid server address (\"exit\" to exit)")
                address = input()
        self._address = address.rstrip("/")
        return True

    # Активирует клиент.
    def run(self, address=""):
        self._active_now = True
        self._connect(address)
        if self._active_now:
            self._print_greeting()
            while self._active_now:
                self._get_user_command()

    # Выход из текущих режимов и деактивация клиента.
    def _exit(self):
        if self._game_mode:
            result = self._end_game(self._game, dict_args=None, address=self._address)
            self._print_response(result)
        if self._package_mode:
            result = self._save_package(self._package, dict_args=None, address=self._address)
            self._print_response(result)
        self._print_farewell()
        self._active_now = False

    # Печать помощи по команде command или в целом по парсеру (если command == None).
    def _print_help(self, command=None):
        try:
            if command:
                self._current_parser.parse_args([command, "--help"])
            else:
                self._current_parser.parse_args(["--help"])
        except SystemExit:
            pass

    # Печать приветствия клиента.
    @staticmethod
    def _print_greeting():
        print("Game Manager \"What? Where? When?\"")
        print("Enter a command (\"--help\" for a list of commands, \"exit\" to exit)")

    # Печать прощания клиента.
    @staticmethod
    def _print_farewell():
        print("Goodbye!")

    # Получение команды от пользователя.
    def _get_user_command(self):
        print(self._command_line, end="")
        command_args = shlex.split(input())
        self._connect(self._address)
        self._handle_command(command_args)

    # Обработка команды пользователя.
    def _handle_command(self, command_args):
        try:
            if "--help" in command_args or "-h" in command_args:
                self._print_help(command_args[0])
            elif command_args[0] == "exit":
                self._exit()
            else:
                args = self._current_parser.parse_args(command_args)
                function = vars(args).pop("function")
                if self._current_parser.object != None:
                    dict_response = function(self._current_parser.object, vars(args), self._address)
                else:
                    dict_response = function(vars(args), self._address)
                self._print_response(dict_response)
        except ParserException:
            pass

    # Печать текста, который вернула функция, выполнявшая команду.
    @staticmethod
    def _print_response(dict_response):
        try:
            print(dict_response["text"])
        except KeyError:
            print("Unknown response.")

    # Добавление пакета к базе (через несколько вопросов).
    def _add_package(self, dict_args=None, address=None):
        self._package_mode = True
        self._package = Package()
        response = self._package.activate(dict_args, address)
        if response["status"] == "OK":
            self._set_current_parser(self._parsers["package_parser"], self._package)
        return response

    def _save_package(self, package, dict_args=None, address=None):
        self._package_mode = False
        self._package = None
        self._set_current_parser(self._parsers["default_parser"], self_object=None)
        response = package.save(dict_args, address)
        return response

    # Создание игры.
    def _create_game(self, dict_args=None, address=None):
        self._game_mode = True
        self._game = Game()
        response = self._game.activate(dict_args, address)
        if response["status"] == "OK":
            self._set_current_parser(self._parsers["game_parser"], self._game)
        return response

    # Окончание игры (с возможным сохранением) и переход в обычный режим.
    def _end_game(self, game, dict_args=None, address=None):
        self._game_mode = False
        self._game = None
        self._set_current_parser(self._parsers["default_parser"], self_object=None)
        args = {}
        while True:
            try:
                print("Save the game? (y/n, default = y): ", end="")
                answer = input()
                args = self._parsers["service_parser"].parse_args(["--bool_answer", answer])
                break
            except ParserException:
                continue
        if args.bool_answer == "y":
            response = Game.save(game, dict_args, address)
            return response
        else:
            return {"text": "Game wasn't saved."}
        # TODO: определить поведение на сервере для сохранения игры.

    # Установка парсера (нужно для специальных режимов; здесь принимается аргумент self_object, который передается в качетсве параметра self в функции, выполняющие команды, например, add_participant в Game).
    def _set_current_parser(self, parser, self_object=None):
        self._current_parser = parser
        self._current_parser.object = self_object
        if parser == self._parsers["default_parser"]:
            self._command_line = "> "
        else:
            self._command_line = ">> "
            try:
                self._print_help()
            except ParserException:
                pass

    def _init_parsers(self):
        parsers = dict()
        parsers["default_parser"] = self._init_default_parser()
        parsers["game_parser"] = self._init_game_parser()
        parsers["service_parser"] = self._init_service_parser()
        parsers["package_parser"] = self._init_package_parser()
        return parsers

    def _init_default_parser(self):
        default_parser = NonExitArgumentParser()

        default_subparsers = default_parser.add_subparsers(dest='command')

        add_question_parser = default_subparsers.add_parser("add_question",
                                                                          help="Add question to database")
        add_question_parser.add_argument("--text", "-t", type=str, help="The text of the question", required=True)
        add_question_parser.add_argument("--answer", "-a", type=str, help="The answer to the question", required=True)
        add_question_parser.add_argument("--name", type=str, help="The name of the question")
        add_question_parser.add_argument("--date", type=datetime.datetime, help="The date of the question")
        add_question_parser.add_argument("--author", type=str, help="The author of the question")
        add_question_parser.add_argument("--complexity", "-c", type=str, help="The complexity of the question")
        add_question_parser.set_defaults(function=Question.add_question)

        add_package_parser = default_subparsers.add_parser("add_package",
                                                                         help="Add package to database")
        add_package_parser.add_argument("--name", type=str, help="The name of the package")
        add_package_parser.add_argument("--date", type=datetime.datetime, help="The date of the package")
        add_package_parser.add_argument("--author", type=str, help="The author of the package")
        add_package_parser.add_argument("--complexity", type=str, help="The complexity of the package")
        add_package_parser.set_defaults(function=self._add_package)

        create_game_parser = default_subparsers.add_parser("create_game",
                                                                         help="Create a new game")
        create_game_parser.set_defaults(function=self._create_game)

        return default_parser

    def _init_game_parser(self):
        game_parser = NonExitArgumentParser()
        game_subparsers = game_parser.add_subparsers(dest='command')

        add_participant_parser = game_subparsers.add_parser("add_participant",
                                                                          help="Add one participant")
        add_participant_parser.add_argument("name", type=str, help="The name of the participant")
        add_participant_parser.set_defaults(function=Game.add_participant)

        add_points_parser = game_subparsers.add_parser("add_points",
                                                                     help="Add points to the participant")
        add_points_parser.add_argument("name", type=str, help="The name of the participant")
        add_points_parser.add_argument("points", type=int, help="The number of points")
        add_points_parser.set_defaults(function=Game.add_points)

        show_table_parser = game_subparsers.add_parser("show_table",
                                                                     help="Show game table")
        show_table_parser.set_defaults(function=Game.show_table)

        get_question_parser = game_subparsers.add_parser("get_question",
                                                       help="Get one question from the base")
        get_question_parser.set_defaults(function=Game.get_question)

        get_answer_parser = game_subparsers.add_parser("get_answer",
                                                       help="Get the answer to the previous question")
        get_answer_parser.set_defaults(function=Game.get_answer)

        end_game_parser = game_subparsers.add_parser("end",
                                                       help="Exit game mode")
        end_game_parser.set_defaults(function=self._end_game)

        load_previous_parser = game_subparsers.add_parser("load_previous",
                                                     help="Load previous game instead of this one (note: without saving)")
        load_previous_parser.set_defaults(function=Game.load_previous)
        return game_parser

    def _init_package_parser(self):
        package_parser = NonExitArgumentParser()
        package_subparsers = package_parser.add_subparsers(dest='command')

        save_package_parser = package_subparsers.add_parser("save", help="Save the package")
        save_package_parser.set_defaults(function=self._save_package)

        add_question_parser = package_subparsers.add_parser("add_question",
                                                            help="Add question to the package")
        add_question_parser.add_argument("--text", "-t", type=str, help="The text of the question", required=True)
        add_question_parser.add_argument("--answer", "-a", type=str, help="The answer to the question", required=True)
        add_question_parser.add_argument("--name", type=str, help="The name of the question")
        add_question_parser.add_argument("--date", type=datetime.datetime, help="The date of the question")
        add_question_parser.add_argument("--author", type=str, help="The author of the question")
        add_question_parser.add_argument("--complexity", "-c", type=str, help="The complexity of the question")
        add_question_parser.set_defaults(function=Package.add_question)

        return package_parser

    # Специальный парсер для обработки не-команд (ответа y/n к примеру).
    def _init_service_parser(self):
        service_parser = NonExitArgumentParser()
        service_parser.add_argument("--bool_answer", choices=["y", "n"], default="y")

        return service_parser


if __name__ == "__main__":
    client = Client()
    client.run(address="")
