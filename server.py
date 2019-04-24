import flask
import json
import argparse


class Server:
    def __init__(self):
        self._app = flask.Flask("What? Where? When?")

        @self._app.route("/", methods=["GET"])
        def _connect():
            return json.dumps({"result_info": {"text": "Connection established"}}), 200

        @self._app.route('/add_question', methods=['POST'])
        def _add_question():
            # TODO: database and package mode.
            return json.dumps({"result_info": {"text": "The question was added.", "status": "OK"}}), 200

        @self._app.route('/package/activate', methods=['POST'])
        def _activate_package():
            # TODO: database and package mode.
            return json.dumps({"result_info": {"text": "Package mode is activated.", "status": "OK"}}), 200

        @self._app.route('/package/add_question', methods=['POST'])
        def _add_question_package():
            # TODO: database and package mode.
            return json.dumps({"result_info": {"text": "The question was added to the package.", "status": "OK"}}), 200

        @self._app.route('/package/save', methods=['POST'])
        def _save_package():
            # TODO: database and package mode.
            return json.dumps({"result_info": {"text": "Package was saved.", "status": "OK"}}), 200

        @self._app.route("/game/get_question", methods=["GET"])
        def _get_question():
            # TODO: database and logic.
            question = "Why did the chicken cross the road?"
            return json.dumps({"result_info": {"text": "The question was shown."}, "question": question}), 200

        @self._app.route("/game/get_answer", methods=["GET"])
        def _get_answer():
            # TODO: database and logic.
            answer = "To get to the other side."
            return json.dumps({"result_info": {"text": "The answer was shown."}, "answer": answer}), 200

        @self._app.route("/game/add_participant", methods=["POST"])
        def _add_participant():
            # TODO: database.
            return json.dumps({"result_info": {"text": "Participant was added."}}), 200

        @self._app.route("/game/add_points", methods=["POST"])
        def _add_points():
            # TODO: database.
            return json.dumps({"result_info": {"text": "Points were added."}}), 200

        # Демонстрация того, как должна выглядеть таблица.
        @self._app.route('/game/show_table', methods=['GET'])
        def _show_table():
            participants = {"Pavel": 50, "Alexey": 150, "Dasha": 35}  # TODO: database.
            return json.dumps({"result_info": {"text": "Table was shown."}, "participants": participants}), 200

        @self._app.route('/game/save', methods=['POST'])
        def _save_game():
            # TODO: database.
            return json.dumps({"result_info": {"text": "Game was saved."}}), 200

        @self._app.route('/game/load_previous', methods=['POST'])
        def _load_previous_game():
            # TODO: database.
            return json.dumps({"result_info": {"text": "Previous game was loaded."}}), 200

        @self._app.route('/game/activate', methods=['POST'])
        def _activate_game():
            # TODO: database.
            return json.dumps({"result_info": {"text": "The game is running.", "status": "OK"}}), 200

    def run(self, port=5000):
        self._app.run('::', port, debug=True, threaded=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()
    server = Server()
    server.run(5000)
