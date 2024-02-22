import os
from uuid import UUID

from typing import Callable

from flask import Flask, Response, make_response, redirect, render_template, request
from dotenv import load_dotenv

from database import DBHelper



load_dotenv()

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.jinja_env.auto_reload = True

database = DBHelper(os.environ['PG_HOST'], int(os.environ['PG_PORT']), os.environ['PG_USER'], os.environ['PG_PASSWD'], os.environ['PG_DB'])


# TODO: Декоратор проверки аутентификации
def Authentication(f: Callable[[UUID], Response]) -> Callable[[], Response]:

    def wrapper() -> Response:
        return f(None)

    wrapper.__name__ = f.__name__
    return wrapper



# Разделы модуля

# TODO: Страница аутентификации
@app.route('/')
def index() -> Response:
    try:
        login: str = request.args['login']
        password: str = request.args['password']
    except KeyError as e:
        return make_response(e)
    return redirect(users.__name__) # type: ignore


# Страница "Список пользователей"
@app.route('/users')
@Authentication
def users(user_id: UUID) -> Response:
    return make_response(render_template('users.html'))


# Страница "Список групп"
@app.route('/groups')
@Authentication
def groups(user_id: UUID) -> Response:
    return make_response(render_template('groups.html'))


# Страница "Список курсов"
@app.route('/courses')
@Authentication
def courses(user_id: UUID) -> Response:
    return make_response(render_template('courses.html'))


# Страница "Добавление в группу"
@app.route('/add_to_group')
@Authentication
def add_to_group(user_id: UUID) -> Response:
    return make_response(render_template('add_to_group.html'))


# Страница "Редактирование курса"
@app.route('/course_edit')
@Authentication
def course_edit(user_id: UUID) -> Response:
    return make_response(render_template('course_edit.html'))


# Страница "Информация о группе"
@app.route('/group_info')
@Authentication
def group_info(user_id: UUID) -> Response:
    return make_response(render_template('group_info.html'))


# Страница "Информация о заданиях"
@app.route('/tasks_info')
@Authentication
def tasks_info(user_id: UUID) -> Response:
    return make_response(render_template('tasks_info.html'))



# API методы

# TODO: Получение списка всех пользователей
@app.post('/api/get_users')
def get_users(user_id: UUID) -> Response:
    return make_response()


# TODO: Получение списка всех курсов
@app.post('/api/get_courses')
def get_courses(user_id: UUID) -> Response:
    return make_response()


# TODO: Получение списка всех групп
@app.post('/api/get_groups')
def get_groups(user_id: UUID) -> Response:
    return make_response()


app.run(host=os.environ['LISTEN_ADDR'], port=int(os.environ['LISTEN_PORT']), debug=True)
