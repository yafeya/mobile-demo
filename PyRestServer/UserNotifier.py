from flask_socketio import SocketIO, emit
from user import User
import json
from preserver import UserPreserver


class UserNotifier:

    __socket_io__: SocketIO = None
    __clients__ = list()

    def __init__(self, socketio: SocketIO):
        self.__socket_io__ = socketio
        self.__socket_io__.on_event('connection', self.on_connected)

    def on_connected(self, message):
        self.__clients__.append(message)
        preserver = UserPreserver()
        users = preserver.load()
        self.notify(users)

    def notify(self, users: [User]):
        if self.__has_handlers__():
            array = []
            for usr in users:
                if type(usr) is User:
                    usr_json = json.dumps(usr.__dict__)
                    array.append(usr_json)
            emit('users', array, broadcast=True)

    def __has_handlers__(self):
        return len(self.__clients__) > 0
