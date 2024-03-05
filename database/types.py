from __future__ import annotations as _annotations
import typing as _typing
import dataclasses as _dataclasses

import uuid as _uuid

import database as _database
import database.enums as _enums
import database.types as _types



@_dataclasses.dataclass
class User:

    id: _uuid.UUID
    login: str
    role: _enums.UserRole
    name: str
    _balance: int | None
    scoring_system: _enums.ScoringSystem | None

    @property
    def balance(self) -> float | None:
        return self._balance / 100 if self._balance is not None else None

    @staticmethod
    def parse(row: tuple) -> _types.User:
        return _types.User(row[0], row[1], _enums.UserRole.parse(row[2]), row[3], row[4], _enums.ScoringSystem.parse(row[5]) if row[5] else None)

    def as_dict(self) -> dict[str, _typing.Any]:
        return {
            'id': str(self.id),
            'login': self.login,
            'role': self.role.value,
            'name': self.name,
            'balance': self.balance,
            'scoring_system': self.scoring_system.value if self.scoring_system else None,
        }


@_dataclasses.dataclass
class UserPassworded(User):

    password: str

    @staticmethod
    def parse(row: tuple) -> _types.UserPassworded:
        return _types.UserPassworded(row[0], row[1], _enums.UserRole.parse(row[3]), row[4], row[5], _enums.ScoringSystem.parse(row[6]) if row[6] else None, row[2])

    def to_user(self) -> User:
        return User(self.id, self.login, self.role, self.name, self._balance, self.scoring_system)


@_dataclasses.dataclass
class Group:

    id: _uuid.UUID
    course_id: _uuid.UUID
    curator_id: _uuid.UUID
    title: str

    @staticmethod
    def parse(row: tuple) -> _types.Group:
        return _types.Group(row[0], row[1], row[2], row[3])

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        if depth == 0 or not database:
            return {
                'id': str(self.id),
                'course_id': str(self.course_id),
                'curator_id': str(self.curator_id),
                'title': self.title,
            }
        else:
            depth -= 1
            return {
                'id': str(self.id),
                'course': i.as_dict(database, depth) if (i := database.get_course(self.course_id)) else None,
                'curator': i.as_dict() if (i := database.get_user(self.curator_id)) else None,
                'title': self.title,
            }


@_dataclasses.dataclass
class Course:

    id: _uuid.UUID
    author_id: _uuid.UUID
    _price: int | None
    title: str
    description: str | None

    @property
    def price(self) -> float | None:
        return self._price / 100 if self._price is not None else None

    @staticmethod
    def parse(row: tuple) -> _types.Course:
        return _types.Course(row[0], row[1], row[2], row[3], row[4])

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        if depth == 0 or not database:
            return {
                'id': str(self.id),
                'author_id': str(self.author_id),
                'price': self.price,
                'title': self.title,
                'description': self.description,
            }
        else:
            depth -= 1
            return {
                'id': str(self.id),
                'author': i.as_dict() if (i := database.get_user(self.author_id)) else None,
                'price': self.price,
                'title': self.title,
                'description': self.description,
            }


@_dataclasses.dataclass
class GroupMember:

    group_id: _uuid.UUID
    student_id: _uuid.UUID

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        if depth == 0 or not database:
            return {
                'group_id': str(self.group_id),
                'student_id': str(self.student_id),
            }
        else:
            depth -= 1
            return {
                'group': i.as_dict(database, depth) if (i := database.get_group(self.group_id)) else None,
                'student': i.as_dict() if (i := database.get_user(self.student_id)) else None,
            }


@_dataclasses.dataclass
class Lesson:

    id: _uuid.UUID
    course_id: _uuid.UUID
    teacher_id: _uuid.UUID
    title: str
    text: str | None

    @staticmethod
    def parse(row: tuple) -> _types.Lesson:
        return _types.Lesson(row[0], row[1], row[2], row[3], row[4])

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        if depth == 0 or not database:
            return {
                'id': str(self.id),
                'course_id': str(self.course_id),
                'teacher_id': str(self.teacher_id),
                'title': self.title,
                'text': self.text,
            }
        else:
            depth -= 1
            return {
                'id': str(self.id),
                'course': i.as_dict(database, depth) if (i := database.get_course(self.course_id)) else None,
                'teacher': i.as_dict() if (i := database.get_user(self.teacher_id)) else None,
                'title': self.title,
                'text': self.text,
            }


@_dataclasses.dataclass
class Task:

    id: _uuid.UUID
    lesson_id: _uuid.UUID
    title: str
    description: str | None

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        # TODO
        if depth == 0 or not database or True:
            return {
                'id': str(self.id),
                'lesson_id': str(self.lesson_id),
                'title': self.title,
                'description': self.description,
            }
        else:
            depth -= 1


@_dataclasses.dataclass
class HomeTask:

    id: _uuid.UUID
    task_id: _uuid.UUID
    student_id: _uuid.UUID
    title: str
    text: str | None
    status: _enums.TaskStatus

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        # TODO
        if depth == 0 or not database or True:
            return {
                'id': str(self.id),
                'task_id': str(self.task_id),
                'student_id': str(self.student_id),
                'title': self.title,
                'text': self.text,
                'status': self.status.value,
            }
        else:
            depth -= 1


@_dataclasses.dataclass
class Deadline:

    group_id: _uuid.UUID
    lesson_id: _uuid.UUID
    deadline: str      # TODO: проверить возвращаемый тип

    def as_dict(self, database: _database.DBHelper | None = None, depth: int = 0) -> dict[str, _typing.Any]:
        # TODO
        if depth == 0 or not database or True:
            return {
                'group_id': str(self.group_id),
                'lesson_id': str(self.lesson_id),
                'deadline': self.deadline,
            }
        else:
            depth -= 1
