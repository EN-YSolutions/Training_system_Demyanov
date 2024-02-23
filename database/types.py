from __future__ import annotations as _annotations
from typing import Any as _Any
from dataclasses import dataclass as _dataclass

from uuid import UUID as _UUID

import database.enums as _enums
import database.types as _types



@_dataclass
class User:

    id: _UUID
    login: str
    role: _enums.UserRole
    name: str
    balance: float | None
    scoring_system: _enums.ScoringSystem | None

    @staticmethod
    def parse(row: tuple) -> _types.User:
        return _types.User(row[0], row[1], _enums.UserRole.parse(row[2]), row[3], float(row[4][2:]) if row[4] else None, _enums.ScoringSystem.parse(row[5]) if row[5] else None)

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'login': self.login,
            'role': self.role.value,
            'name': self.name,
            'balance': self.balance,
            'scoring_system': self.scoring_system.value if self.scoring_system else None,
        }


@_dataclass
class UserPassworded(User):

    password: str

    @staticmethod
    def parse(row: tuple) -> _types.UserPassworded:
        return _types.UserPassworded(row[0], row[1], _enums.UserRole.parse(row[3]), row[4], float(row[5][2:]) if row[5] else None, _enums.ScoringSystem.parse(row[6]) if row[6] else None, row[2])

    def to_user(self) -> User:
        return User(self.id, self.login, self.role, self.name, self.balance, self.scoring_system)



@_dataclass
class Group:

    id: _UUID
    course_id: _UUID
    curator_id: _UUID
    title: str

    @staticmethod
    def parse(row: tuple) -> _types.Group:
        return _types.Group(row[0], row[1], row[2], row[3])

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'course_id': str(self.course_id),
            'curator_id': str(self.curator_id),
            'title': self.title,
        }


@_dataclass
class Course:

    id: _UUID
    author_id: _UUID
    price: float | None
    title: str
    description: str | None

    @staticmethod
    def parse(row: tuple) -> _types.Course:
        return _types.Course(row[0], row[1], float(row[2][2:]), row[3], row[4])

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'author_id': str(self.author_id),
            'price': self.price,
            'title': self.title,
            'description': self.description,
        }


@_dataclass
class GroupMember:

    group_id: _UUID
    student_id: _UUID

    def as_dict(self) -> dict[str, _Any]:
        return {
            'group_id': str(self.group_id),
            'student_id': str(self.student_id),
        }


@_dataclass
class Lesson:

    id: _UUID
    course_id: _UUID
    teacher_id: _UUID
    title: str
    text: str | None

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'course_id': str(self.course_id),
            'teacher_id': str(self.teacher_id),
            'title': self.title,
            'text': self.text,
        }


@_dataclass
class Task:

    id: _UUID
    lesson_id: _UUID
    title: str
    description: str | None

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'lesson_id': str(self.lesson_id),
            'title': self.title,
            'description': self.description,
        }


@_dataclass
class HomeTask:

    id: _UUID
    task_id: _UUID
    student_id: _UUID
    title: str
    text: str | None
    status: _enums.TaskStatus

    def as_dict(self) -> dict[str, _Any]:
        return {
            'id': str(self.id),
            'task_id': str(self.task_id),
            'student_id': str(self.student_id),
            'title': self.title,
            'text': self.text,
            'status': self.status.value,
        }


@_dataclass
class Deadline:

    group_id: _UUID
    lesson_id: _UUID
    deadline: str      # TODO: проверить возвращаемый тип

    def as_dict(self) -> dict[str, _Any]:
        return {
            'group_id': str(self.group_id),
            'lesson_id': str(self.lesson_id),
            'deadline': self.deadline,
        }
