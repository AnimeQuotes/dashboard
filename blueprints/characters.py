import os

from bson import ObjectId
from flask import Blueprint, request, redirect, url_for, flash, abort, g, \
    render_template, send_from_directory

from db.models import Image, Character
from utils import requires_authentication
from utils.constants import RE_CHARACTER_NAME, RE_CHARACTER_ANIME, STORAGE_PATH


characters = Blueprint("characters", __name__, url_prefix="/characters")


@characters.route("/")
@requires_authentication()
def list_characters():
    return render_template("pages/characters/list.html", characters=Character.objects)


@characters.route("/add", methods=["GET", "POST"])
@requires_authentication()
def add_character():
    if request.method == "POST":
        name = request.form.get("name")
        if not name or not RE_CHARACTER_NAME.match(name):
            flash("Invalid character name.")
            return redirect(url_for(".add_character"))

        anime = request.form.get("anime")
        if not anime or not RE_CHARACTER_ANIME.match(anime):
            flash("Invalid anime title.")
            return redirect(url_for(".add_character"))

        character = Character(name=name, anime=anime, author=g.user).save()

        return redirect(url_for(".view_character", character_id=character.id))

    return render_template("pages/characters/add.html")


@characters.route("/<character_id>/delete")
@requires_authentication(admin=True)
def delete_character(character_id):
    character = Character.objects(id=character_id).first()
    if character is None:
        abort(404)

    Image.objects(character=character).delete()
    character.delete()

    flash("Character removed.")
    return redirect(url_for(".list_characters"))


@characters.route("/<character_id>", methods=["GET", "POST"])
@requires_authentication()
def view_character(character_id):
    character = Character.objects(id=character_id).first()
    if character is None:
        abort(404)

    return render_template(
        "pages/characters/view.html",
        character=character,
        images=Image.objects(character=character).order_by("-date")
    )


@characters.route("/<character_id>/upload", methods=["POST"])
@requires_authentication()
def upload_image(character_id):
    character = Character.objects(id=character_id).first()
    if character is None:
        abort(404)

    try:
        file = request.files["image"]
    except KeyError:
        flash("No file uploaded.")
        return redirect(url_for(".view_character", character_id=character_id))

    if file.filename == "":
        flash("No file uploaded.")
        return redirect(url_for(".view_character", character_id=character_id))
    if file.mimetype not in {"image/jpeg", "image/png"}:
        flash("File must be in 'jpeg' or 'png' format.")
        return redirect(url_for(".view_character", character_id=character_id))

    if not os.path.exists(STORAGE_PATH):
        os.makedirs(STORAGE_PATH)

    dirs = os.listdir(STORAGE_PATH)
    if not dirs:
        storage_path = os.path.join(STORAGE_PATH, "1".zfill(3))
        os.mkdir(storage_path)
    else:
        dirs.sort(key=int)

        storage_path = os.path.join(STORAGE_PATH, dirs[-1])
        if len(os.listdir(storage_path)) >= 500:
            storage_path = os.path.join(STORAGE_PATH, str(int(dirs[-1]) + 1).zfill(3))
            os.mkdir(storage_path)

    file_id = ObjectId()
    file_path = os.path.join(storage_path, str(file_id) + "." + file.mimetype.split("/")[1])

    file.save(file_path)
    Image(path=file_path, character=character, uploader=g.user).save()

    flash("Image added.")
    return redirect(url_for(".view_character", character_id=character_id))


@characters.route("/images/<image_id>/delete")
@requires_authentication()
def delete_image(image_id):
    image = Image.objects(id=image_id).first()
    if image is None:
        abort(404)

    if not g.user.is_admin or image.uploader != g.user:
        abort(403)

    os.remove(image.path)
    image.delete()

    flash("Image removed.")
    return redirect(url_for(".view_character", character_id=image.character.id))


@characters.route("/images/<image_id>")
def display_image(image_id):
    image = Image.objects(id=image_id).first()
    if image is None:
        abort(404)

    path = image.path.split(os.sep)
    directory = os.sep.join(path[:-1])
    filename = path[-1]

    return send_from_directory(directory, filename)
