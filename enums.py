from enum import Enum as _Enum



class HTTP(_Enum):
    OK = 200

    BadRequest = 400
    Unauthorized = 401
    NotFound = 404

    InternalServerError = 500
    NotImplemented = 501


class ErrorText(_Enum):
    InternalServerError = 'internal server error'
    InvalidRequestFormat = 'invalid request format'
    NotImplementedYet = 'not implemented yet'

    NotEnoughArguments = 'not enough arguments'
    InvalidArgumentValue = 'invalid argument value'

    AuthenticationCookieNotFound = 'authentication cookie not found'
    InvalidTokenSignature = 'invalid token signature'
    TokenHasExpired = 'token has expired'
    InvalidToken = 'invalid token'

    UserNotFound = 'user not found'
    GroupNotFound = 'group not found'
    CourseNotFound = 'course not found'
