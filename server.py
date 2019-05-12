import flask
import json
import argparse
from database import *
from peewee import *
from datetime import datetime, date


class Server:
    def __init__(self):
        self._app = flask.Flask("What? Where? When?")
        self._package_mode = False
        self._current_game = None
        self._current_package = None
        self._current_question = None

        @self._app.route("/", methods=["GET"])
        def _connect():
            return json.dumps({"result_info": {"text": "Connection established"}})

        @self._app.route('/add_question', methods=['POST'])
        def _add_question():
            args = flask.request.json
            try:
                question = DataBaseQuestion(**args)
                question.save()
                return json.dumps({"result_info": {"text": "The question was added.", "status": "OK"}})
            except IntegrityError as err:
                return json.dumps({"result_info": {"text": "The question wasn't added.", "reason": err.args[0], "status": "BAD"}})

        @self._app.route('/package/activate', methods=['POST'])
        def _activate_package():
            args = flask.request.json

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
            args = flask.request.json
            try:
                question = DataBaseQuestion(**args, package=self._current_package)
                question.save()
                return json.dumps({"result_info": {"text": "The question was added.", "status": "OK"}})
            except IntegrityError as err:
                return json.dumps({"result_info": {"text": "The question wasn't added.", "reason": err.args[0],
                                                   "status": "BAD"}})

        @self._app.route('/package/save', methods=['POST'])
        def _save_package():
            self._current_package.save()
            self._current_package = None
            return json.dumps({"result_info": {"text": "Package was saved.", "status": "OK"}})

        @self._app.route('/game/lost_package', methods=['POST'])
        def _lost_package():
            self._current_package = None
            return json.dumps({"result_info": {"text": "Package mode has been reset.", "status": "OK"}})

        @self._app.route("/game/get_question", methods=["POST"])
        def _get_question():
            args = flask.request.json
            subq = DataBaseQuestion.select().where(DataBaseQuestion.id.not_in(self._used_questions))
            if self._current_package is not None:
                subq = subq.select().where(DataBaseQuestion.package == self._current_package)

            for key, value in args.items():
                if value is not None and getattr(DataBaseQuestion, key, None) is not None:
                    subq = subq.where(getattr(DataBaseQuestion, key) == value)
            try:
                question = DataBaseQuestion.raw("SELECT * from ({0}) AS subq offset floor(random() * (SELECT COUNT(*) FROM ({0}) AS subq)) limit 1 ;".format(subq.sql()[0]), *subq.sql()[1], *subq.sql()[1]).get()
                self._used_questions.add(question.id)
                self._current_question = question
                if question.package is not None:
                    package_name = question.package.name
                else:
                    package_name = None
                return json.dumps({"result_info": {"text": "The question was shown.", "status": "OK"}, "text": question.text, "author": question.author, "complexity": question.complexity, "package": package_name, "name": question.name})
            except Exception as err:
                return json.dumps({"result_info": {"text": "The question wasn't shown.", "reason": err.args[0],
                                                   "status": "BAD"}})

        @self._app.route("/game/get_package", methods=["POST"])
        def _get_package():
            args = flask.request.json
            subq = DataBasePackage.select().where(DataBasePackage.id.not_in(self._used_packages))
            for key, value in args.items():
                if value is not None and getattr(DataBasePackage, key, None) is not None:
                    subq = subq.where(getattr(DataBasePackage, key) == value)
            try:
                package = DataBasePackage.raw("SELECT * from ({0}) AS subq offset floor(random() * (SELECT COUNT(*) FROM ({0}) AS subq)) limit 1 ;".format(
                        subq.sql()[0]), *subq.sql()[1], *subq.sql()[1]).get()
                self._current_package = package
                self._used_packages.add(package.id)
                return json.dumps(
                    {"result_info": {"text": "The package was found.", "status": "OK"}, "author": package.author,
                     "complexity": package.complexity, "name": package.name})
            except Exception as err:
                return json.dumps({"result_info": {"text": "The package wasn't found.", "reason": err.args[0],
                                                   "status": "BAD"}})

        @self._app.route("/game/get_answer", methods=["GET"])
        def _get_answer():
            if hasattr(self, "_current_question"):
                return json.dumps({"result_info": {"text": "The answer was shown.", "status": "OK"}, "answer": self._current_question.answer, "comment": self._current_question.comment}), 200
            else:
                return json.dumps(
                    {"result_info": {"text": "The answer wasn't shown.", "status": "BAD", "reason": "The question was not got."},
                     })

        @self._app.route("/game/add_participant", methods=["POST"])
        def _add_participant():
            args = flask.request.json
            table = json.loads(self._current_game.table)
            if args["name"] not in table:
                table[args["name"]] = 0
                self._current_game.table = json.dumps(table)
                return json.dumps({"result_info": {"text": "Participant was added.", "status": "OK"}})
            else:
                return json.dumps({"result_info": {"text": "Participant wasn't added.", "status": "BAD", "reason": "A participant with that name is already in the table."}})

        @self._app.route("/game/add_points", methods=["POST"])
        def _add_points():
            args = flask.request.json
            table = json.loads(self._current_game.table)
            if args["name"] in table:
                table[args["name"]] += args["points"]
                self._current_game.table = json.dumps(table)
                return json.dumps({"result_info": {"text": "Points were added.", "status": "OK"}})
            else:
                return json.dumps({"result_info": {"text": "Points weren't added.", "status": "BAD",
                                                   "reason": "A participant with that name isn't in the table."}})

        @self._app.route('/game/show_table', methods=['GET'])
        def _show_table():
            return json.dumps({"result_info": {"text": "Table was shown.", "status": "OK"}, "table": json.loads(self._current_game.table)})

        @self._app.route('/game/save', methods=['POST'])
        def _save_game():
            self._current_game.date = date.today()
            self._current_game.time = datetime.now().time()
            try:
                previous_game = DataBaseGame.select().where(DataBaseGame.previous is True).get()
                previous_game.previous = False
                previous_game.save()
            except Exception as err:
                pass
            self._current_game.previous = True
            self._current_game.save()
            return json.dumps({"result_info": {"text": "Game was saved.", "status": "OK"}})

        @self._app.route('/game/load_previous', methods=['POST'])
        def _load_previous_game():
            args = flask.request.json
            subq = DataBaseGame.select()
            if not(args["name"] or args["date"]):
                subq = subq.where(DataBaseGame.previous is True)
            if args["name"]:
                subq = subq.where(DataBaseGame.name == args["name"])
            if args["date"]:
                try:
                    date = datetime.strptime(args["date"], "%Y/%m/%d")
                except:
                    return json.dumps({"result_info": {"text": "Previous game wasn't loaded.", "status": "BAD",
                                                       "reason": "Incorrect date format."}})
                subq = subq.where(DataBaseGame.date == date).order_by(DataBaseGame.time.desc())
            try:
                previous_game = subq.get()
                self._current_game = previous_game
                return json.dumps({"result_info": {"text": "Previous game was loaded.", "status": "OK"}})
            except:
                return json.dumps({"result_info": {"text": "Previous game wasn't loaded.", "status": "BAD",
                                           "reason": "There is no saved game with these characteristics."}})

        @self._app.route('/game/activate', methods=['POST'])
        def _activate_game():
            args = flask.request.json
            if args["name"] and DataBaseGame.select().where(DataBaseGame.name == args["name"]).exists():
                return json.dumps({"result_info": {"text": "The game isn't running.", "status": "BAD",
                                                   "reason": "Game with that name is already in the database."}})
            self._current_game = DataBaseGame(**args)
            self._current_package = None
            self._used_packages = set()
            self._used_questions = set()
            return json.dumps({"result_info": {"text": "The game is running.", "status": "OK"}})

    def run(self, database_configs_file, port=5000, host='127.0.0.1'):
        with open(database_configs_file) as json_configs:
            database_configs = json.loads(json_configs.read())
        self._db = init_database(database_configs)
        self._app.run(host, port, debug=True, threaded=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='127.0.0.1')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--db_configs', type=str, default="database_configs.json")
    args = parser.parse_args()
    server = Server()
    server.run(args.db_configs, args.port, args.host)
