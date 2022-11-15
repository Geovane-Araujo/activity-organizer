import werkzeug.exceptions


class InternalServer(werkzeug.exceptions.HTTPException):
    code = 500
    description = "Internal Error"

