import json
from flask import Blueprint
from werkzeug.exceptions import HTTPException

hubExcept = Blueprint("hubExcept",__name__)


@hubExcept.app_errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
        "success": False
    })
    response.content_type = "application/json"
    return response, e.code

