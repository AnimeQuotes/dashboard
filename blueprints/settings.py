import argon2
from flask import Blueprint, request, redirect, url_for, flash, render_template, g

from utils import requires_authentication
from utils.constants import RE_PASSWORD

settings = Blueprint("settings", __name__, url_prefix="/settings")


@settings.route("/password", methods=["GET", "POST"])
@requires_authentication()
def change_password():
    if request.method == "POST":
        current_password = request.form.get("current-password")
        if not current_password or not RE_PASSWORD.match(current_password):
            flash("Current password is invalid.")
            return redirect(url_for(".change_password"))

        new_password = request.form.get("new-password")
        if not new_password or not RE_PASSWORD.match(new_password):
            flash("New password is invalid.")
            return redirect(url_for(".change_password"))

        ph = argon2.PasswordHasher()
        try:
            ph.verify(g.user.password, current_password)
        except argon2.exceptions.VerifyMismatchError:
            flash("Current password is invalid.")
            return redirect(url_for(".change_password"))

        new_password = ph.hash(new_password)

        g.user.update(password=new_password)
        flash("Password updated.")

        return redirect(url_for(".change_password"))

    return render_template("pages/settings/change_password.html")
