import argon2
from flask import Blueprint, session, request, redirect, url_for, flash, render_template

from db.models import User
from utils.constants import RE_USERNAME, RE_PASSWORD

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if not username or not RE_USERNAME.match(username):
            flash("Invalid username.")
            return redirect(url_for(".login"))

        password = request.form.get("password")
        if not password or not RE_PASSWORD.match(password):
            flash("Invalid password.")
            return redirect(url_for(".login"))

        user = User.objects(username=username).first()
        if user is None:
            flash("User not found.")
            return redirect(url_for(".login"))

        ph = argon2.PasswordHasher()
        try:
            ph.verify(user.password, password)
        except argon2.exceptions.VerifyMismatchError:
            flash("Invalid password.")
            return redirect(url_for(".login"))

        session["username"] = user.username
        session.permanent = True

        return redirect(url_for("characters.list_characters"))

    session.clear()
    return render_template("pages/auth/login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for(".login"))
