
from user import User
import json
from flask_restful import Resource
from flask import request
from UserRepository import UserRepository
from preserver import UserPreserver


class UsersApiController(Resource):

    __user_repository__: UserRepository = None
    __user_preserver__: UserPreserver = None

    def __init__(self, repository: UserRepository, preserver: UserPreserver):
        self.__user_repository__ = repository
        self.__user_preserver__ = preserver

    def put(self):
        # this is for from data
        # parser = reqparse.RequestParser()
        # parser.add_argument('username', type=str)
        # parser.add_argument('password', type=str)
        # parser.add_argument('email', type=str)
        # args = parser.parse_args()

        # this is for raw.
        args = request.get_json(force=True)
        username = args['username']
        password = args['password']
        email = args['email']

        usr = User()
        usr.username = username
        usr.password = password
        usr.email = email

        result = Result()
        if usr is None or usr.username == '':
            result.Success = False
            result.Message = 'Invalid user'
            result.Code = 201
        elif self.__contains_usr__(usr.username):
            result.Success = False
            result.Message = '{arg1} has existed.'.format(arg1=usr.username)
            result.Code = 200
        else:
            self.__user_repository__.add(usr)
            result.Success = True
            result.Message = '{arg1} has been added.'.format(arg1=usr.username)
            result.Code = 200
            self.__user_preserver__.save(self.__user_repository__.get_users())
            j_obj = json.dumps(result.__dict__)
        return j_obj, result.Code

    def post(self):
        # this is for from data
        # parser = reqparse.RequestParser()
        # parser.add_argument('username', type=str)
        # parser.add_argument('password', type=str)
        # parser.add_argument('email', type=str)
        # args = parser.parse_args()

        # this is for raw.
        args = request.get_json(force=True)
        username = args['username']
        password = args['password']
        email = args['email']

        usr = User()
        usr.username = username
        usr.password = password
        usr.email = email

        result = Result()

        if usr is None or usr.username == '':
            result.Success = False
            result.Message = 'Invalid user'
            result.Code = 201
        elif self.__contains_usr__(usr.username):
            self.__user_repository__.update(usr)
            self.__user_preserver__.save(self.__user_repository__.get_users())
            result.Success = True
            result.Message = '{arg1} has been updated'.format(arg1=usr.username)
            result.Code = 200
        else:
            self.__user_repository__.add(usr)
            self.__user_preserver__.save(self.__user_repository__.get_users())
            result.Success = True
            result.Message = '{arg1} has been added'.format(arg1=usr.username)
            result.Code = 200

        j_obj = json.dumps(result.__dict__)
        return j_obj, result.Code

    def get(self):
        users = self.__user_repository__.get_users()
        array = []
        for usr in users:
            if type(usr) is User:
                usr_json = json.dumps(usr.__dict__)
                array.append(usr_json)

        return array, 200

    def __contains_usr__(self, username):
        contains: bool = False
        for usr in self.__user_repository__.get_users():
            if usr.username == username:
                contains = True
                break
        return contains


class UserApiController(Resource):

    __user_repository__: UserRepository = None
    __user_preserver__: UserPreserver = None

    def __init__(self, repository: UserRepository, preserver: UserPreserver):
        self.__user_repository__ = repository
        self.__user_preserver__ = preserver

    def get(self, username: str):
        result = Result()
        if username == '':
            result.Success = False
            result.Code = 201
            result.Message = 'Invalid username'
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code
        elif self.__contains_usr__(username):
            usr = self.__user_repository__.get_user(username)
            j_obj = json.dumps(usr.__dict__)
            return j_obj, 200
        else:
            result.Success = False
            result.Message = '{arg1} is not in repository'.format(arg1=username)
            result.Code = 200
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code

    def delete(self, username: str):
        result = Result()
        if username == '':
            result.Success = False
            result.Code = 201
            result.Message = 'Invalid username'
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code
        elif self.__contains_usr__(username):
            usr = User()
            usr.username = username
            self.__user_repository__.remove(usr)
            self.__user_preserver__.save(self.__user_repository__.get_users())
            result.Success = False
            result.Code = 200
            result.Message = '{arg1} has been delete'.format(arg1=username)
            j_obj = json.dumps(result.__dict__)
            return j_obj, 200
        else:
            result.Success = False
            result.Message = '{arg1} is not in repository'.format(arg1=username)
            result.Code = 200
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code

    def __contains_usr__(self, username):
        contains: bool = False
        for usr in self.__user_repository__.get_users():
            if usr.username == username:
                contains = True
                break
        return contains


class Result(object):
    Success: bool = False
    Message: str = ''
    Code: int = 201