import os

from flask import Flask, Response, jsonify, make_response, render_template
from dotenv import load_dotenv



load_dotenv()

app = Flask(__name__, template_folder='web/templates', static_folder='web/static')
app.jinja_env.auto_reload = True



@app.route('/')
def users() -> Response:
    return make_response(render_template('users.html'))


@app.route('/groups')
def groups() -> Response:
    return make_response(render_template('groups.html'))


@app.route('/courses')
def courses() -> Response:
    return make_response(render_template('courses.html'))


@app.route('/add_to_group')
def add_to_group() -> Response:
    return make_response(render_template('add_to_group.html'))


@app.route('/course_edit')
def course_edit() -> Response:
    return make_response(render_template('course_edit.html'))


@app.route('/group_info')
def group_info() -> Response:
    return make_response(render_template('group_info.html'))


@app.route('/tasks_info')
def tasks_info() -> Response:
    return make_response(render_template('tasks_info.html'))



app.run(host=os.environ['LISTEN_ADDR'], port=int(os.environ['LISTEN_PORT']))
