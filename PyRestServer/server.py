from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_socketio import SocketIO
from UserRepository import UserRepository
from UserNotifier import UserNotifier
from preserver import UserPreserver
from UsersApiController import UserApiController, UsersApiController


app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def start_restful_server():
    user_repository = UserRepository()
    user_preserver = UserPreserver()
    users = user_preserver.load()
    for usr in users:
        user_repository.add(usr)
    controller_args = {'repository': user_repository, 'preserver': user_preserver}
    api.add_resource(UsersApiController, '/users', resource_class_kwargs=controller_args)
    api.add_resource(UserApiController, '/user/<username>', resource_class_kwargs=controller_args)
    # app.run('localhost', 9981, debug=True)
    # run_simple('localhost', 9981, app,
    #            use_reloader=True, use_debugger=True, use_evalex=True)


def start_socket_server():
    socketio.run(app, 'localhost', 9981)


def initialize_notifier():
    notifier = UserNotifier(socketio)


if __name__ == '__main__':
    initialize_notifier()
    start_restful_server()
    start_socket_server()
