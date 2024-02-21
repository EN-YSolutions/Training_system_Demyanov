from enum import Enum
from dataclasses import dataclass

from uuid import UUID
from click import group

import psycopg


class UserRole(Enum):
    Student = 'student'
    Teacher = 'teacher'
    Curator = 'curator'
    Admin = 'admin'


class ScoringSystem(Enum):
    Abstract = 'abstract'
    Points = 'points'


class TaskStatus(Enum):
    NotCompleted = 'not completed'
    Pending = 'pending'
    RevisionNeeded = 'revision_needed'
    Completed = 'completed'
    Failed = 'failed'



@dataclass
class User:
    id: UUID
    login: str
    password: str
    name: str
    role: UserRole
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
    date: str           # TODO: проверить возвращаемый тип
    title: str
    text: str | None


@dataclass
class Task:
    id: UUID
    lesson_id: UUID
    student_id: UUID
    title: str
    description: str | None
    status: TaskStatus
    score: str


@dataclass
class HomeTask:
    id: UUID
    task_id: UUID
    student_id: UUID    # по идее не нужен, т. к. в Task уже есть student_id
    title: str
    text: str | None


@dataclass
class Deadline:
    id: UUID
    group_id: UUID
    lesson_id: UUID
    deadline: str      # TODO: проверить возвращаемый тип


class DBHelper:

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


    def __del__(self):
        self.__database.close()
