import flask
import json
import argparse
from database import *
from peewee import *
from datetime import datetime, date
from enum import Enum


class InputResult(Enum): # Типы ошибок проверки входных данных.
    OK = 0
    TypeError = 1
    KeyError = 2
    EvalError = 3


class Server: # TODO: обрабатывать ошибки, связанные с существованием БД и таблиц.
    NoneType = type(None) # Без понятия, где это лежит в питоне.

    def __init__(self):
        self._app = flask.Flask("What? Where? When?")
        self._package_mode = False
        self._current_game = None
        self._current_package = None
        self._current_question = None

        @self._app.route("/", methods=["GET"])
        def _connect():
            return json.dumps({"result_info": {"text": "Connection established"}})

        @self._app.route("/add_question", methods=["POST"])
        def _add_question():
            args = __get_data(flask.request.json)
            return __add_question(args, None)

        @self._app.route('/package/activate', methods=['POST'])
        def _activate_package():
            args = __get_data(flask.request.json)

            input_mask = {"name": [str], "author": [str, Server.NoneType], "complexity": [int, Server.NoneType]} # Маска для аргументов, передаваемых в функцию.
            input_check = Server.check_client_input(dict_args=args, dict_mask=input_mask)
            if input_check[0] != InputResult.OK:
                return json.dumps(
                    {"result_info": {"text": "Package mode isn't activated.", "reason": input_check[1], "status": "BAD"}})

            try:
                if DataBasePackage.select().where(DataBasePackage.name == args["name"]).exists():
                    return json.dumps({"result_info": {"text": "Package mode isn't activated.", "status": "BAD", "reason": "Package with that name is already in the database."}})
                self._current_package = DataBasePackage(**args)
                self._current_package.save()
                return json.dumps({"result_info": {"text": "Package mode is activated; package: {}".format(args["name"]), "status": "OK"}})
            except IntegrityError as err:
                return json.dumps({"result_info": {"text": "Package mode isn't activated.; package: {}".format(args["name"]), "reason": err.args[0],
                                                   "status": "BAD"}})

        @self._app.route('/package/add_question', methods=['POST'])
        def _add_question_package():
            args = __get_data(flask.request.json)
            if self._current_package is not None:
                return __add_question(args, self._current_package)
            else:
                return json.dumps({"result_info": {"text": "The question wasn't added to the package.", "reason": "Package mode is not activated.",
                                               "status": "BAD"}})

        @self._app.route('/package/save', methods=['POST'])
        def _save_package():
            if self._current_package is not None:
                self._current_package.save()
                self._current_package = None
                return json.dumps({"result_info": {"text": "Package was saved.", "status": "OK"}})
            else:
                return json.dumps({"result_info": {"text": "The package wasn't save.", "reason": "Package mode is not activated.",
                                               "status": "BAD"}})

        @self._app.route('/game/lost_package', methods=['POST'])
        def _lost_package():
            self._current_package = None
            return json.dumps({"result_info": {"text": "Package mode has been reset.", "status": "OK"}})

        @self._app.route("/game/get_question", methods=["POST"])
        def _get_question():
            args = __get_data(flask.request.json)
            subq = DataBaseQuestion.select().where(DataBaseQuestion.id.not_in(self._used_questions))
            if self._current_package is not None:
                subq = subq.select().where(DataBaseQuestion.package == self._current_package)

            for key, value in args.items():
                if value is not None and getattr(DataBaseQuestion, key, None) is not None:
                    subq = subq.where(getattr(DataBaseQuestion, key) == value)
            try:
                question = DataBaseQuestion.raw("SELECT * from ({0}) AS subq offset floor(random() * (SELECT COUNT(*) FROM ({0}) AS subq)) limit 1 ;".format(subq.sql()[0]), *subq.sql()[1], *subq.sql()[1]).get()
            except DoesNotExist:
                return json.dumps({"result_info": {"text": "The question wasn't shown.", "reason": "Questions are over.",
                                               "status": "BAD"}})
            self._used_questions.add(question.id)
            self._current_question = question
            if question.package is not None:
                package_name = question.package.name
            else:
                package_name = None
            return json.dumps({"result_info": {"text": "The question was shown.", "status": "OK"}, "text": question.text, "author": question.author, "complexity": question.complexity, "package": package_name, "name": question.name})


        @self._app.route("/game/get_package", methods=["POST"])
        def _get_package():
            args = __get_data(flask.request.json)
            subq = DataBasePackage.select().where(DataBasePackage.id.not_in(self._used_packages))
            for key, value in args.items():
                if value is not None and getattr(DataBasePackage, key, None) is not None:
                    subq = subq.where(getattr(DataBasePackage, key) == value)
            try:
                package = DataBasePackage.raw("SELECT * from ({0}) AS subq offset floor(random() * (SELECT COUNT(*) FROM ({0}) AS subq)) limit 1 ;".format(
                        subq.sql()[0]), *subq.sql()[1], *subq.sql()[1]).get()
            except DoesNotExist as err:
                return json.dumps({"result_info": {"text": "The package wasn't found.", "reason": "Packages are over.",
                                                   "status": "BAD"}})
            self._current_package = package
            self._used_packages.add(package.id)
            return json.dumps(
                {"result_info": {"text": "The package was found.", "status": "OK"}, "author": package.author,
                 "complexity": package.complexity, "name": package.name})

        @self._app.route("/game/get_answer", methods=["GET"])
        def _get_answer():
            if self._current_question is not None:
                return json.dumps({"result_info": {"text": "The answer was shown.", "status": "OK"}, "answer": self._current_question.answer, "comment": self._current_question.comment}), 200
            else:
                return json.dumps(
                    {"result_info": {"text": "The answer wasn't shown.", "status": "BAD", "reason": "The question was not got."},
                     })

        @self._app.route("/game/add_participant", methods=["POST"])
        def _add_participant():
            if self._current_game is not None:
                args = __get_data(flask.request.json)

                input_mask = {"name": [str]}
                input_check = Server.check_client_input(dict_args=args, dict_mask=input_mask)
                if input_check[0] != InputResult.OK:
                    return json.dumps(
                        {"result_info": {"text": "Participant wasn't added.", "reason": input_check[1], "status": "BAD"}})

                table = json.loads(self._current_game.table)
                if args["name"] not in table:
                    table[args["name"]] = 0
                    self._current_game.table = json.dumps(table)
                    return json.dumps({"result_info": {"text": "Participant was added.", "status": "OK"}})
                else:
                    return json.dumps({"result_info": {"text": "Participant wasn't added.", "status": "BAD", "reason": "A participant with that name is already in the table."}})
            else:
                return json.dumps({"result_info": {"text": "Participant wasn't added.", "status": "BAD",
                                                   "reason": "Game mode is not activated."}})

        @self._app.route("/game/add_points", methods=["POST"])
        def _add_points():
            if self._current_game is not None:
                args = __get_data(flask.request.json)

                input_mask = {"name": [str], "points": [int]}
                input_check = Server.check_client_input(dict_args=args, dict_mask=input_mask)
                if input_check[0] != InputResult.OK:
                    return json.dumps(
                        {"result_info": {"text": "Points weren't added.", "reason": input_check[1], "status": "BAD"}})

                table = json.loads(self._current_game.table)
                if args["name"] in table:
                    table[args["name"]] += args["points"]
                    self._current_game.table = json.dumps(table)
                    return json.dumps({"result_info": {"text": "Points were added.", "status": "OK"}})
                else:
                    return json.dumps({"result_info": {"text": "Points weren't added.", "status": "BAD",
                                                       "reason": "A participant with that name isn't in the table."}})
            else:
                return json.dumps({"result_info": {"text": "Points weren't added.", "status": "BAD",
                                                   "reason": "Game mode is not activated."}})

        @self._app.route('/game/show_table', methods=['GET'])
        def _show_table():
            if self._current_game is not None:
                return json.dumps({"result_info": {"text": "Table was shown.", "status": "OK"}, "table": json.loads(self._current_game.table)})
            else:
                return json.dumps({"result_info": {"text": "Table hasn't been shown.", "status": "BAD", "reason": "Game mode is not activated."}})

        @self._app.route('/game/save', methods=['POST'])
        def _save_game():
            if self._current_game is not None:
                self._current_game.date = date.today()
                self._current_game.time = datetime.now().time()
                try:
                    previous_game = DataBaseGame.select().where(DataBaseGame.previous is True).get()
                    previous_game.previous = False
                    previous_game.save()
                except DoesNotExist as err:
                    pass
                self._current_game.previous = True
                self._current_game.save()
                return json.dumps({"result_info": {"text": "Game was saved.", "status": "OK"}})
            else:
                return json.dumps({"result_info": {"text": "Game hasn't been saved.", "status": "BAD", "reason": "Game mode is not activated."}})

        @self._app.route('/game/load_previous', methods=['POST'])
        def _load_previous_game():
            args = __get_data(flask.request.json)

            input_mask = {"name": [str, Server.NoneType], "date": [str, Server.NoneType]}
            input_check = Server.check_client_input(dict_args=args, dict_mask=input_mask)
            if input_check[0] != InputResult.OK:
                return json.dumps(
                    {"result_info": {"text": "Previous game wasn't loaded.", "reason": input_check[1], "status": "BAD"}})

            subq = DataBaseGame.select()
            if args["name"] is None and args["date"] is None:
                subq = subq.where(DataBaseGame.previous is True)
            if args["name"] is not None:
                subq = subq.where(DataBaseGame.name == args["name"])
            if args["date"] is not None:
                try:
                    date = datetime.strptime(args["date"], "%Y/%m/%d")
                except ValueError:
                    return json.dumps({"result_info": {"text": "Previous game wasn't loaded.", "status": "BAD",
                                                       "reason": "Incorrect date format."}})
                subq = subq.where(DataBaseGame.date == date).order_by(DataBaseGame.time.desc())
            try:
                previous_game = subq.get()
                self._current_game = previous_game
                return json.dumps({"result_info": {"text": "Previous game was loaded.", "status": "OK"}})
            except DoesNotExist:
                return json.dumps({"result_info": {"text": "Previous game wasn't loaded.", "status": "BAD",
                                           "reason": "There is no saved game with these characteristics."}})

        @self._app.route('/game/activate', methods=['POST'])
        def _activate_game():
            args = __get_data(flask.request.json)
            input_mask = {"name": [str, Server.NoneType]}
            input_check = Server.check_client_input(dict_args=args, dict_mask=input_mask)
            if input_check[0] != InputResult.OK:
                return json.dumps(
                    {"result_info": {"text": "Game hasn't been activated.", "reason": input_check[1],
                                     "status": "BAD"}})
            if args["name"] is not None and DataBaseGame.select().where(DataBaseGame.name == args["name"]).exists():
                return json.dumps({"result_info": {"text": "The game isn't running.", "status": "BAD",
                                                   "reason": "Game with that name is already in the database."}})
            self._current_game = DataBaseGame(**args)
            self._current_package = None
            self._used_packages = set()
            self._used_questions = set()
            return json.dumps({"result_info": {"text": "The game is running.", "status": "OK"}})

        def __add_question(dict_args, package=None): # Общая функция для добавления вопросов в пакетном режиме и в обычном (вызывается из соответствующих _add_question_package и _add_question).
            input_mask = {"text": [str], "comment": [str, Server.NoneType], "answer": [str],
                          "name": [str, Server.NoneType], "author": [str, Server.NoneType],
                          "complexity": [int, Server.NoneType]}
            input_check = Server.check_client_input(dict_args=dict_args, dict_mask=input_mask)
            if input_check[0] != InputResult.OK:
                return json.dumps(
                    {"result_info": {"text": "The question wasn't added.", "reason": input_check[1], "status": "BAD"}})

            try:
                question = DataBaseQuestion(**dict_args, package=package)
                question.save()
                return json.dumps({"result_info": {"text": "The question was added.", "status": "OK"}})
            except IntegrityError as err:
                return json.dumps({"result_info": {"text": "The question wasn't added.", "reason": err.args[0],
                                                   "status": "BAD"}})

        def __get_data(dict_args): # На тот случай, если json вообще не будет в качестве аргумента.
            if dict_args is None:
                return {}
            else:
                return dict_args

    def run(self, database_configs_file, port=5000, host='127.0.0.1'):
        with open(database_configs_file) as json_configs:
            database_configs = json.loads(json_configs.read())
        self._db = init_database(database_configs)
        self._app.run(host, port, debug=True, threaded=True)

    @staticmethod
    def check_client_input(dict_args, dict_mask, list_eval=[]): # Проверяет входные данные на соответствие маске. Для примера: dict_mask = {'name': ['string', None], 'points': ['int', 'float']}
        for key, type_list in dict_mask.items():
            if not key in dict_args:
                return (InputResult.KeyError, "Incorrect data, missing key = {}.".format(key))
            if not any(isinstance(dict_args[key], type_key) for type_key in type_list):
                return (InputResult.TypeError, "Incorrect data, key = {} must be of {} type instead of {} type.".format(key, type_list, type(dict_args[key])))
        for expression in list_eval:
            try:
                eval(expression)
            except Exception:
                return (InputResult.EvalError, "Incorrect data, An error occurred while trying to work with the data. The data is probably in the wrong input format.")
        return (InputResult.OK, "Correct data.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--db_configs', type=str, default="database_configs.json")
    args = parser.parse_args()
    server = Server()
    server.run(args.db_configs, args.port, args.host)
