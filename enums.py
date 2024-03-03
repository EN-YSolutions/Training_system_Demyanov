from enum import Enum as _Enum



class HTTP(_Enum):
    OK = 200

    BadRequest = 400
    Unauthorized = 401
    Forbidden = 403
    NotFound = 404

    InternalServerError = 500
    NotImplemented = 501


class ErrorText(_Enum):
    InternalServerError = 'Внутренняя ошибка сервера'
    InvalidRequestFormat = 'Неверный формат запроса'
    NotImplementedYet = 'Ещё не реализовано'

    NotEnoughArguments = 'Недостаточно аргументов'
    InvalidArgumentValue = 'Неверное значение аргумента'

    AuthenticationCookieNotFound = 'cookie аутентификации не найдена'
    InvalidTokenSignature = 'Неверная подпись токена'
    TokenHasExpired = 'Срок действия токена истек'
    InvalidToken = 'Недействительный токен'

    AccessDenied = 'Доступ запрещён'

    UserNotFound = 'Пользователь не найден'
    GroupNotFound = 'Группа не найдена'
    CourseNotFound = 'Курс не найден'
