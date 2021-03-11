import argon2
from flask import Blueprint, request, redirect, url_for, flash, g, render_template

from db.models import User
from utils import requires_authentication
from utils.constants import RE_USERNAME, RE_PASSWORD

users = Blueprint("users", __name__, url_prefix="/users")


@users.route("/")
@requires_authentication(admin=True)
def list_users():
    return render_template("pages/users/list.html", users=User.objects)


@users.route("/add", methods=["GET", "POST"])
@requires_authentication(admin=True)
def add_user():
    if request.method == "POST":
        username = request.form.get("username")
        if not username or not RE_USERNAME.match(username):
            flash("Invalid username.")
            return redirect(url_for(".add_user"))

        password = request.form.get("password")
        if not password or not RE_PASSWORD.match(password):
            flash("Invalid password.")
            return redirect(url_for(".add_user"))

        if User.objects(username=username).first() is not None:
            flash(f"Username already exists.")
            return redirect(url_for(".add_user"))

        ph = argon2.PasswordHasher()
        pw = ph.hash(password)

        User(username=username, password=pw).save()
        flash("User created.")

        return redirect(url_for(".add_user"))

    return render_template("pages/users/add.html")


@users.route("/<user_id>/delete")
@requires_authentication(admin=True)
def delete_user(user_id):
    user = User.objects(id=user_id).first()
    if user is None:
        flash("User not found.")
        return redirect(url_for(".list_users"))
    if user.id == g.user.id:
        flash("You can not delete your own user.")
        return redirect(url_for(".list_users"))

    user.delete()
    flash("User deleted.")

    return redirect(url_for(".list_users"))
