from datetime import datetime
from functools import wraps

from flask import abort, session, request, redirect, url_for, g

from db.models import User


def requires_authentication(*, admin: bool = False, token: str = None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if token is not None:
                authorization = request.headers.get("Authorization")
                if authorization != token:
                    abort(401)
            else:
                username = session.get("username")
                if username is None:
                    return redirect(url_for("auth.login"))

                user = User.objects(username=username).first()
                if user is None:
                    session.clear()
                    return redirect(url_for("auth.login"))

                user.update(last_seen=datetime.utcnow())

                if admin and not user.is_admin:
                    abort(403)

                g.user = user

            rv = f(*args, **kwargs)
            return rv
        return decorated
    return decorator
