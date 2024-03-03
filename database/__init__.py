from __future__ import annotations as _annotations

import uuid as _uuid

import bcrypt as _bcrypt
import psycopg as _psycopg

import database.types as _types
import database.enums as _enums
import database.exceptions as _exceptions



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
            cursor.execute(open('database/sql/create_types.sql').read()) # type: ignore
            cursor.execute(open('database/sql/create_tables.sql').read()) # type: ignore


    def __db_connect(self, host: str, port: int, user: str, password: str, dbname: str | None = None):
        if dbname:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)
        else:
            self.__database = _psycopg.connect(f'host={host} port={port} user={user} password={password}', autocommit=True)



    # -------------------------------------------------- Аутентификация --------------------------------------------------

    def auth_user(self, login: str, password: str) -> _types.User:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_USERS}
                WHERE "login" = %s
            ''', (login, ))
            passworded_user: _types.UserPassworded | None = _types.UserPassworded.parse(result) if (result := cursor.fetchone()) else None

        if not passworded_user:
            raise _exceptions.UserNotFoundException

        if not _bcrypt.checkpw(password.encode(), passworded_user.password.encode()):
            raise _exceptions.UserNotFoundException

        return passworded_user.to_user()



    # -------------------------------------------------- Пользователи --------------------------------------------------

    def get_all_users(self) -> list[_types.User]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "id", "login", "role", "name", "balance", "scoring_system"
                FROM {DBHelper.__TABLE_USERS}
            ''')
            return [_types.User.parse(row) for row in cursor.fetchall()]


    def get_user(self, user_id: _uuid.UUID) -> _types.User:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "id", "login", "role", "name", "balance", "scoring_system"
                FROM {DBHelper.__TABLE_USERS}
                WHERE "id" = %s
            ''', (user_id, ))
            user: _types.User | None = (_types.User.parse(result) if (result := cursor.fetchone()) else None)

        if not user:
            raise _exceptions.UserNotFoundException

        return user


    def get_user_groups(self, user_id: _uuid.UUID) -> list[_types.Group]:

        self.get_user(user_id)

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS_MEMBERS}
                WHERE "student_id" = %s
            ''', (user_id, ))
            groups_ids: list[_uuid.UUID] = [row[0] for row in cursor.fetchall()]

        groups: list[_types.Group] = []
        for group_id in groups_ids:
            if (i := self.get_group(group_id)):
                groups.append(i)

        return groups



    # -------------------------------------------------- Группы --------------------------------------------------

    def get_all_groups(self) -> list[_types.Group]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS}
            ''')
            return [_types.Group.parse(row) for row in cursor.fetchall()]


    def get_group(self, group_id: _uuid.UUID) -> _types.Group:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_GROUPS}
                WHERE "id" = %s
            ''', (group_id, ))
            group: _types.Group | None = _types.Group.parse(result) if (result := cursor.fetchone()) else None

        if not group:
            raise _exceptions.GroupNotFoundException

        return group


    def get_group_members(self, group_id: _uuid.UUID) -> list[_types.User]:

        self.get_group(group_id)

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "student_id"
                FROM {DBHelper.__TABLE_GROUPS_MEMBERS}
                WHERE "group_id" = %s
            ''', (group_id, ))
            users_ids: list[_uuid.UUID] = [row[0] for row in cursor.fetchall()]

        result: list[_types.User] = []
        for user_id in users_ids:
            if (i := self.get_user(user_id)):
                result.append(i)

        return result


    def get_group_members_amount(self, group_id) -> int:

        self.get_group(group_id)

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT COUNT("student_id")
                FROM {DBHelper.__TABLE_GROUPS_MEMBERS}
                WHERE "group_id" = %s
            ''', (group_id, ))
            return int(result[0]) if (result := cursor.fetchone()) else 0


    def add_group_member(self, group_id: _uuid.UUID, user_id: _uuid.UUID) -> _types.User:

        self.get_group(group_id)
        user: _types.User = self.get_user(user_id)

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO {DBHelper.__TABLE_GROUPS_MEMBERS} ("group_id", "student_id")
                VALUES (%s, %s)
            ''', (group_id, user_id))

        return user


    def delete_group_member(self, group_id: _uuid.UUID, user_id: _uuid.UUID) -> _types.User:

        self.get_group(group_id)
        user: _types.User | None = self.get_user(user_id)

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                DELETE FROM {DBHelper.__TABLE_GROUPS_MEMBERS}
                WHERE "group_id" = %s AND "student_id" = %s
            ''', (group_id, user_id))

        return user



    # -------------------------------------------------- Курсы --------------------------------------------------

    def get_all_courses(self) -> list[_types.Course]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_COURSES}
            ''')
            return [_types.Course.parse(row) for row in cursor.fetchall()]


    def get_course(self, course_id: _uuid.UUID) -> _types.Course:

        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT *
                FROM {DBHelper.__TABLE_COURSES}
                WHERE "id" = %s
            ''', (course_id, ))
            course: _types.Course | None = _types.Course.parse(result) if (result := cursor.fetchone()) else None

        if not course:
            raise _exceptions.CourseNotFoundException

        return course


    # ----------------------------------------------------------------------------------------------------



    def __del__(self):
        self.__database.close()
        DBHelper.__instance = None
