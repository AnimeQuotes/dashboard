import json
import traceback
from typing import Union

from flask import Blueprint, request, jsonify, abort, make_response, send_file
from werkzeug.exceptions import HTTPException, InternalServerError

from db.models import Character, Image
from utils import requires_authentication, generate_quote_image
from utils.constants import API_TOKEN

api = Blueprint("api", __name__, url_prefix="/api")


@api.before_request
def before_request():
    if not request.is_json:
        abort(415)


@api.errorhandler(Exception)
def handle_exception(e: Union[Exception, HTTPException]):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description
        })
        response.content_type = "application/json"

        return response

    traceback.print_exception(type(e), e, e.__traceback__)

    e = InternalServerError
    return jsonify(code=e.code, name="Internal Server Error", description=e.description), 500


@api.route("/generate")
@requires_authentication(token=API_TOKEN)
def generate():
    quote = request.args.get("quote")
    if not quote:
        abort(400, description="Missing 'quote' parameter.")

    meta = Image.objects().aggregate({"$sample": {"size": 1}}).next()
    character = Character.objects(id=meta["character"]).only("name", "anime").first()
    image = generate_quote_image(author=character.name, quote=quote, image_path=meta["path"])

    if type(image) is str:
        abort(400, description=image)

    response = send_file(image, mimetype="image/png")
    response.headers["Character"] = character.name
    response.headers["Anime"] = character.anime
    return response
