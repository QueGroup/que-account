class AuthExceptionCodes:
    """Auth errors codes mapping class"""

    USER_ALREADY_EXISTS: int = 3000
    USER_NOT_FOUND: int = 3001
    USER_DEACTIVATED: int = 3002
    USER_UNAUTHORIZED: int = 3003
    PROVIDED_PASSWORD_INCORRECT: int = 3004
    INVALID_PROVIDED_TOKEN: int = 3005
    TOKEN_NOT_FOUND: int = 3006
