
from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user, login_required


def role_required(*allowed_roles):
    """Restrict a route to authenticated users with an allowed role."""

    def decorator(view_function):
        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):
            if current_user.role not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("catalogue"))

            return view_function(*args, **kwargs)

        return wrapped_view

    return decorator
