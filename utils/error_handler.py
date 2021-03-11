from flask import render_template
from werkzeug.exceptions import HTTPException


def handle_exception(e: HTTPException):
    return render_template("pages/error.html", error=e), e.code
