import werkzeug.exceptions


class Unauthorized(werkzeug.exceptions.HTTPException):
    code = 401
    description = "token is required"

