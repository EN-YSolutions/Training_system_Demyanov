import bcrypt as _bcrypt
import psycopg as _psycopg

import database.types as _types
import database.enums as _enums



class DBHelper:

    __TABLE_USERS = 'users'
    __TABLE_GROUPS = 'groups'
    __TABLE_COURSES = 'courses'
    __TABLE_GROUPS_MEMBERS = 'groups_members'
    __TABLE_LESSONS = 'lessons'
    __TASKS = 'tasks'
    __HOME_TASKS = 'home_tasks'
    __DEADLINES = 'deadlines'


    def __db_connect(self, host: str, port: int, user: str, password: str, dbname: str | None = None):
        if dbname:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)
        else:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password}', autocommit=True)


    def __init__(self, host: str, port: int, user: str, password: str, dbname: str) -> None:

        self.__db_connect(host, port, user, password)
        try:
            self.__database.execute(f'CREATE DATABASE "{dbname}"') # type: ignore
        except _psycopg.errors.DuplicateDatabase:
            pass

        self.__db_connect(host, port, user, password, dbname)

        with self.__database.cursor() as cursor:
            cursor.execute(open('sql/create_types.sql').read()) # type: ignore
            cursor.execute(open('sql/create_tables.sql').read()) # type: ignore


    def auth_user(self, login: str, password: str) -> _types.User | None:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_USERS}
                WHERE "login" = %s
                LIMIT 1
            ''', (login, ))
            passworded_user: _types.UserPassworded | None = _types.UserPassworded.parse(result) if (result := cursor.fetchone()) else None

        if not passworded_user:
            return None

        if not _bcrypt.checkpw(password.encode(), passworded_user.password.encode()):
            return None

        return passworded_user.to_user()


    def get_all_users(self) -> list[_types.User]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "id", "login", "role", "name", "balance", "scoring_system"
                FROM {DBHelper.__TABLE_USERS}
            ''')
            return [_types.User.parse(row) for row in cursor.fetchall()]


    def get_all_groups(self) -> list[_types.Group]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS}
            ''')
            return [_types.Group.parse(row) for row in cursor.fetchall()]


    def get_all_courses(self) -> list[_types.Course]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_COURSES}
            ''')
            return [_types.Course.parse(row) for row in cursor.fetchall()]


    def __del__(self):
        self.__database.close()
