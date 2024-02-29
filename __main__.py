from typing import Callable, Any

import os
import ssl
import time
import json
from uuid import UUID

import jwt
import dotenv
from flask import Flask, Response, make_response, redirect, url_for, render_template, request

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
    r = make_response(json.dumps({'ok': True, 'result': result}, indent=2))
    r.content_type = 'application/json'
    return r


def APIError(http_code: int, description: str) -> Response:
    r = make_response(json.dumps({'ok': False, 'description': description}), http_code)
    r.content_type = 'application/json'
    return r



# Страница аутентификации
@app.get('/')
def index() -> Response:

    if 'auth_token' in request.cookies:
        return make_response(redirect(url_for(users.__name__)))

    return make_response(render_template('index.html'))


# Выход из аккаунта (кука httpOnly не доступна в JS на стороне клиента, нужно удалять на стороне сервера)
@app.get('/logout')
def logout() -> Response:
    r: Response = make_response(redirect(url_for(index.__name__)))
    r.set_cookie('auth_token', '', expires=0, domain='project.wg', secure=True, httponly=True)
    return r



# Страница "Список пользователей"
@app.get('/users')
def users() -> Response:
    return make_response(render_template('users.html'))


# Страница с информацией о конкретном пользователе
@app.get('/user')
def user() -> Response:
    return make_response(render_template('user.html'))



# Страница "Список групп"
@app.get('/groups')
def groups() -> Response:
    return make_response(render_template('groups.html'))


# Страница с информацией о конкретной группе
@app.get('/group')
def group() -> Response:
    return make_response(render_template('group.html'))



# Страница "Список курсов"
@app.get('/courses')
def courses() -> Response:
    return make_response(render_template('courses.html'))


# Страница с информацией о конкретном курсе
@app.get('/course')
def course() -> Response:
    return make_response(render_template('course.html'))



# Страница "Добавление в группу"
@app.get('/add_to_group')
def add_to_group() -> Response:
    return make_response(render_template('add_to_group.html'))


# Страница "Редактирование курса"
@app.get('/course_edit')
def course_edit() -> Response:
    return make_response(render_template('course_edit.html'))


# Страница "Информация о группе"
@app.get('/group_info')
def group_info() -> Response:
    return make_response(render_template('group_info.html'))


# Страница "Информация о заданиях"
@app.get('/tasks_info')
def tasks_info() -> Response:
    return make_response(render_template('tasks_info.html'))





# -------------------------------------------------- Аутентификация --------------------------------------------------

# Аутентификация
@app.post('/api/login')
def login() -> Response:

    try:
        login: str = request.form['login']
        password: str = request.form['password']
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    if not (user := database.auth_user(login, password)):
        return APIError(HTTP.NotFound.value, ErrorText.UserNotFound.value)

    if user.role != UserRole.Admin:
        return APIError(HTTP.Forbidden.value, ErrorText.AccessDenied.value)

    t: int = int(time.time())
    r: Response = make_response(APIResult({}))
    r.set_cookie('auth_token', jwt.encode({'sub': str(user.id), 'iat': t, 'exp': t+86400}, app.secret_key), domain='project.wg', secure=True, httponly=True)

    return r





# -------------------------------------------------- Пользователи --------------------------------------------------

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
        user_id: UUID = UUID(request.form['id'])
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


# Получение списка групп, в которых состоит пользователь
@app.post('/api/get_user_groups')
@Authentication
def get_user_groups(token: dict[str, Any]) -> Response:

    try:
        user_id: UUID = UUID(request.form['id'])
        depth: int = int(request.form['depth'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        groups: list[Group] = database.get_user_groups(user_id)
        return APIResult({'groups': [i.as_dict(database, depth) for i in groups]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Удаление пользователя из группы
@app.post('/api/delete_user_group')
@Authentication
def delete_user_group(token: dict[str, Any]) -> Response:

    try:
        user_id: UUID = UUID(request.form['user_id'])
        group_id: UUID = UUID(request.form['group_id'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        database.delete_user_group(user_id, group_id)
        return APIResult({})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)





# -------------------------------------------------- Группы --------------------------------------------------

# Получение списка всех групп
@app.post('/api/get_groups')
@Authentication
def get_groups(token: dict[str, Any]) -> Response:

    try:
        depth: int = int(request.form['depth'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        groups: list[Group] = database.get_all_groups()
        return APIResult({'entries': [{'group': i.as_dict(database, depth), 'members': database.get_group_members_amount(i.id)} for i in groups]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение группы по ID
@app.post('/api/get_group')
@Authentication
def get_group(token: dict[str, Any]) -> Response:

    try:
        group_id: UUID = UUID(request.form['id'])
        depth: int = int(request.form['depth'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        group: Group | None = database.get_group(group_id)
        if group:
            return APIResult({'group': group.as_dict(database, depth)})
        else:
            return APIError(HTTP.NotFound.value, ErrorText.GroupNotFound.value)
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


@app.post('/api/get_group_members')
@Authentication
def get_group_members(token: dict[str, Any]) -> Response:

    try:
        group_id: UUID = UUID(request.form['id'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        users: list[User] = database.get_group_members(group_id)
        return APIResult({'users': [i.as_dict() for i in users]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)





# -------------------------------------------------- Курсы --------------------------------------------------

# Получение списка всех курсов
@app.post('/api/get_courses')
@Authentication
def get_courses(token: dict[str, Any]) -> Response:

    try:
        depth: int = int(request.form['depth'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        courses: list[Course] = database.get_all_courses()
        return APIResult({'courses': [i.as_dict(database, depth) for i in courses]})
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)


# Получение курса по ID
@app.post('/api/get_course')
@Authentication
def get_course(token: dict[str, Any]) -> Response:

    try:
        course_id: UUID = UUID(request.form['id'])
        depth: int = int(request.form['depth'])
    except:
        return APIError(HTTP.BadRequest.value, ErrorText.InvalidRequestFormat.value)

    try:
        course: Course | None = database.get_course(course_id)
        if course:
            return APIResult({'course': course.as_dict(database, depth)})
        else:
            return APIError(HTTP.NotFound.value, ErrorText.CourseNotFound.value)
    except:
        return APIError(HTTP.InternalServerError.value, ErrorText.InternalServerError.value)





app.run(host=os.environ['LISTEN_ADDR'], port=int(os.environ['LISTEN_PORT']), ssl_context=ctx, debug=True)
