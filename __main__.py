from typing import Callable, Any

import os
import ssl
import time
import json
from uuid import UUID

import jwt
import dotenv
from flask import Flask, Response, make_response, redirect, render_template, request

from database import *
from database.types import *
from database.enums import *
from enums import HTTP, ErrorText



dotenv.load_dotenv()

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.secret_key = os.environ['JWT_SECRET']
app.jinja_env.auto_reload = True

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(os.environ['TLS_CERT'], os.environ['TLS_KEY'])

database = DBHelper(os.environ['PG_HOST'], int(os.environ['PG_PORT']), os.environ['PG_USER'], os.environ['PG_PASSWD'], os.environ['PG_DB'])


# Декоратор проверки аутентификации
def Authentication(f: Callable[[dict[str, Any]], Response]) -> Callable[[], Response]:

    def wrapper() -> Response:

        try:
            raw_token = request.cookies['auth_token']
        except:
            return APIError(HTTP.Unauthorized.value, ErrorText.AuthenticationCookieNotFound.value)

        try:
            token: dict[str, Any] = jwt.decode(raw_token, app.secret_key, algorithms=[jwt.get_unverified_header(raw_token)['alg']])
        except jwt.InvalidSignatureError:
            return APIError(HTTP.Unauthorized.value, ErrorText.InvalidTokenSignature.value)
        except jwt.ExpiredSignatureError:
            return APIError(HTTP.Unauthorized.value, ErrorText.TokenHasExpired.value)
        except jwt.DecodeError:
            return APIError(HTTP.Unauthorized.value, ErrorText.InvalidToken.value)

        return f(token)

    wrapper.__name__ = f.__name__
    return wrapper


def APIResult(result: dict[str, Any]) -> Response:
    r = make_response(json.dumps({'ok': True, 'result': result}))
    r.content_type = 'application/json'
    return r


def APIError(http_code: int, description: str) -> Response:
    r = make_response(json.dumps({'ok': False, 'description': description}), http_code)
    r.content_type = 'application/json'
    return r


# Разделы модуля

# TODO: Страница аутентификации
@app.route('/')
def index() -> Response:

    try:
        login: str = request.args['login']
        password: str = request.args['password']
    except:
        return make_response('Не указан логин или пароль')

    if not (user := database.auth_user(login, password)):
        return make_response('Неправильный пароль или такого пользователя не существует')

    r: Response = make_response(redirect(users.__name__))
    t: int = int(time.time())
    r.set_cookie('auth_token', jwt.encode({'sub': str(user.id), 'iat': t, 'exp': t+86400}, app.secret_key), domain='project.wg', secure=True, httponly=True)

    return r


# Страница "Список пользователей"
@app.route('/users')
def users() -> Response:
    return make_response(render_template('users.html'))


# Страница "Список групп"
@app.route('/groups')
def groups() -> Response:
    return make_response(render_template('groups.html'))


# Страница "Список курсов"
@app.route('/courses')
def courses() -> Response:
    return make_response(render_template('courses.html'))


# Страница "Добавление в группу"
@app.route('/add_to_group')
def add_to_group() -> Response:
    return make_response(render_template('add_to_group.html'))


# Страница "Редактирование курса"
@app.route('/course_edit')
def course_edit() -> Response:
    return make_response(render_template('course_edit.html'))


# Страница "Информация о группе"
@app.route('/group_info')
def group_info() -> Response:
    return make_response(render_template('group_info.html'))


# Страница "Информация о заданиях"
@app.route('/tasks_info')
def tasks_info() -> Response:
    return make_response(render_template('tasks_info.html'))



# API методы

# Получение списка всех пользователей
@app.post('/api/get_users')
@Authentication
def get_users(token: dict[str, Any]) -> Response:
    try:
        users: list[User] = database.get_all_users()
        return APIResult({'users': [i.as_dict() for i in users]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение пользователя по ID
@app.post('/api/get_user')
@Authentication
def get_user(token: dict[str, Any]) -> Response:

    try:
        user_id: UUID = UUID(request.form['user_id'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        user: User | None = database.get_user(user_id)
        if user:
            return APIResult({'user': user.as_dict()})
        else:
            return APIError(HTTP.NotFound.value, ErrorText.UserNotFound.value)
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение списка всех групп
@app.post('/api/get_groups')
@Authentication
def get_groups(token: dict[str, Any]) -> Response:
    try:
        groups: list[Group] = database.get_all_groups()
        return APIResult({'groups': [i.as_dict(database) for i in groups]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение группы по ID
@app.post('/api/get_group')
@Authentication
def get_group(token: dict[str, Any]) -> Response:

    try:
        group_id: UUID = UUID(request.form['group_id'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        group: Group | None = database.get_group(group_id)
        if group:
            return APIResult({'group': group.as_dict(database)})
        else:
            return APIError(HTTP.NotFound.value, ErrorText.GroupNotFound.value)
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение списка всех курсов
@app.post('/api/get_courses')
@Authentication
def get_courses(token: dict[str, Any]) -> Response:
    try:
        courses: list[Course] = database.get_all_courses()
        return APIResult({'courses': [i.as_dict(database) for i in courses]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение курса по ID
@app.post('/api/get_course')
@Authentication
def get_course(token: dict[str, Any]) -> Response:

    try:
        course_id: UUID = UUID(request.form['course_id'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        course: Course | None = database.get_course(course_id)
        if course:
            return APIResult({'course': course.as_dict(database)})
        else:
            return APIError(HTTP.NotFound.value, ErrorText.CourseNotFound.value)
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


app.run(host=os.environ['LISTEN_ADDR'], port=int(os.environ['LISTEN_PORT']), ssl_context=ctx, debug=True)
