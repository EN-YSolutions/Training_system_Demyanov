from __future__ import annotations as _annotations

from enum import Enum as _Enum



class UserRole(_Enum):

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


class ScoringSystem(_Enum):

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


class TaskStatus(_Enum):

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
