from __future__ import annotations as _annotations
from typing import Self

import uuid as _uuid

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
    __TABLE_TASKS = 'tasks'
    __TABLE_HOME_TASKS = 'home_tasks'
    __TABLE_DEADLINES = 'deadlines'

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


    def __db_connect(self, host: str, port: int, user: str, password: str, dbname: str | None = None):
        if dbname:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)
        else:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password}', autocommit=True)


    def auth_user(self, login: str, password: str) -> _types.User | None:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_USERS}
                WHERE "login" = %s
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


    def get_user(self, user_id: _uuid.UUID) -> _types.User | None:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "id", "login", "role", "name", "balance", "scoring_system"
                FROM {DBHelper.__TABLE_USERS}
                WHERE "id" = %s
            ''', (user_id, ))
            return _types.User.parse(result) if (result := cursor.fetchone()) else None


    def get_all_groups(self) -> list[_types.Group]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS}
            ''')
            return [_types.Group.parse(row) for row in cursor.fetchall()]


    def get_group(self, group_id: _uuid.UUID) -> _types.Group | None:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS}
                WHERE "id" = %s
            ''', (group_id, ))
            return _types.Group.parse(result) if (result := cursor.fetchone()) else None


    def get_group_members(self, group_id: _uuid.UUID) -> list[_types.User]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "student_id"
                FROM {DBHelper.__TABLE_GROUPS_MEMBERS}
                WHERE "group_id" = %s
            ''', (group_id, ))
            users_ids: list[_uuid.UUID] = [row[0] for row in cursor.fetchall()]

        result: list[_types.User] = []
        for user_id in users_ids:
            user: _types.User | None = self.get_user(user_id)
            if user:
                result.append(user)

        return result


    def get_all_courses(self) -> list[_types.Course]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_COURSES}
            ''')
            return [_types.Course.parse(row) for row in cursor.fetchall()]


    def get_course(self, course_id: _uuid.UUID) -> _types.Course | None:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_COURSES}
                WHERE "id" = %s
            ''', (course_id, ))
            return _types.Course.parse(result) if (result := cursor.fetchone()) else None


    def __del__(self):
        self.__database.close()
        DBHelper.__instance = None
