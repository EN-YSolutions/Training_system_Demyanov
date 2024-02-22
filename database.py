from __future__ import annotations


from uuid import UUID

from enum import Enum
from dataclasses import dataclass

import psycopg



class UserRole(Enum):

    Student = 'student'
    Teacher = 'teacher'
    Curator = 'curator'
    Admin = 'admin'

    @staticmethod
    def parse(value: str) -> UserRole:
        match value:
            case UserRole.Student.value:
                return UserRole.Student
            case UserRole.Teacher.value:
                return UserRole.Teacher
            case UserRole.Curator.value:
                return UserRole.Curator
            case UserRole.Admin.value:
                return UserRole.Admin
            case _:
                raise ValueError(f'Unknown user role: {value}')


class ScoringSystem(Enum):

    Abstract = 'abstract'
    Points = 'points'

    @staticmethod
    def parse(value: str) -> ScoringSystem:
        match value:
            case ScoringSystem.Abstract.value:
                return ScoringSystem.Abstract
            case ScoringSystem.Points.value:
                return ScoringSystem.Points
            case _:
                raise ValueError(f'Unknown scoring system: {value}')


class TaskStatus(Enum):

    NotCompleted = 'not completed'
    Pending = 'pending'
    NeedsRevision = 'needs revision'
    Correct = 'correct'
    Incorrect = 'incorrect'

    @staticmethod
    def parse(value: str) -> TaskStatus:
        match value:
            case TaskStatus.NotCompleted.value:
                return TaskStatus.NotCompleted
            case TaskStatus.Pending.value:
                return TaskStatus.Pending
            case TaskStatus.NeedsRevision.value:
                return TaskStatus.NeedsRevision
            case TaskStatus.Correct.value:
                return TaskStatus.Correct
            case TaskStatus.Incorrect.value:
                return TaskStatus.Incorrect
            case _:
                raise ValueError(f'Unknown task status: {value}')



@dataclass
class User:
    id: UUID
    login: str
    role: UserRole
    name: str
    balance: float | None
    scoring_system: ScoringSystem | None


@dataclass
class Course:
    id: UUID
    author_id: UUID
    price: float | None
    title: str
    description: str | None


@dataclass
class Group:
    id: UUID
    course_id: UUID
    curator_id: UUID
    title: str


@dataclass
class GroupMember:
    group_id: UUID
    student_id: UUID


@dataclass
class Lesson:
    id: UUID
    course_id: UUID
    teacher_id: UUID
    title: str
    text: str | None


@dataclass
class Task:
    id: UUID
    lesson_id: UUID
    title: str
    description: str | None


@dataclass
class HomeTask:
    id: UUID
    task_id: UUID
    student_id: UUID
    title: str
    text: str | None
    status: TaskStatus


@dataclass
class Deadline:
    group_id: UUID
    lesson_id: UUID
    deadline: str      # TODO: проверить возвращаемый тип



class DBHelper:

    __TABLE_USERS = 'users'
    __TABLE_COURSES = 'courses'
    __TABLE_GROUPS = 'groups'
    __TABLE_GROUPS_MEMBERS = 'groups_members'
    __TABLE_LESSONS = 'lessons'
    __TASKS = 'tasks'
    __HOME_TASKS = 'home_tasks'
    __DEADLINES = 'deadlines'


    def __db_connect(self, host: str, port: int, user: str, password: str, dbname: str | None = None):
        if dbname:
            self.__database = psycopg.connect(f'host={host} port={port} user={user} password={password} dbname={dbname}', autocommit=True)
        else:
            self.__database = psycopg.connect(f'host={host} port={port} user={user} password={password}', autocommit=True)


    def __init__(self, host: str, port: int, user: str, password: str, dbname: str) -> None:

        self.__db_connect(host, port, user, password)
        try:
            self.__database.execute(f'CREATE DATABASE "{dbname}"') # type: ignore
        except psycopg.errors.DuplicateDatabase:
            pass

        self.__db_connect(host, port, user, password, dbname)

        with self.__database.cursor() as cursor:
            cursor.execute(open('sql/create_types.sql').read()) # type: ignore
            cursor.execute(open('sql/create_tables.sql').read()) # type: ignore


    def get_all_users(self) -> list[User]:
        with self.__database.cursor() as cursor:
            cursor.execute(f'''
                SELECT "id", "login", "role", "name", "balance", "scoring_system"
                from {DBHelper.__TABLE_USERS}
            ''')
            return [User(row[0], row[1], UserRole.parse(row[2]), row[3], float(row[4][2:]), ScoringSystem.parse(row[5])) for row in cursor.fetchall()]


    def __del__(self):
        self.__database.close()
