from enum import Enum as _Enum



class HTTP(_Enum):
    OK = 200

    BadRequest = 400
    Unauthorized = 401
    NotFound = 404

    InternalServerError = 500
    NotImplemented = 501


class ErrorText(_Enum):
    NotImplementedYet = 'not implemented yet'
    InvalidRequestFormat = 'invalid request format'

    AuthenticationCookieNotFound = 'authentication cookie not found'
    InvalidTokenSignature = 'invalid token signature'
    TokenHasExpired = 'token has expired'
    InvalidToken = 'invalid token'

    InternalServerError = 'internal server error'

    NotEnoughArguments = 'not enough arguments'
    InvalidArgumentValue = 'invalid argument value'
