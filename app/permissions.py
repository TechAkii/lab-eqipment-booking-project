
# Imports wraps to preserve the original function's metadata when applying decorators.
from functools import wraps

# Imports Flask functions for displaying messages and redirecting users.
from flask import flash, redirect, url_for

# Imports the current logged-in user and the decorator that requires authentication.
from flask_login import current_user, login_required


# Creates a decorator that restricts route access to users with specified roles.
def role_required(*allowed_roles):
    """Restrict a route to authenticated users with an allowed role."""

    # Defines the decorator that receives the route function.
    def decorator(view_function):
        # Preserves the route function's metadata and requires the user to be logged in.
        @wraps(view_function)
        @login_required
        def wrapped_view(*args, **kwargs):
            # Checks whether the logged-in user's role is permitted to access the route.
            if current_user.role not in allowed_roles:
                # Displays an error message and redirects unauthorized users to the catalogue.
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("catalogue"))

            # Executes the original route function when the user's role is allowed.
            return view_function(*args, **kwargs)

        # Returns the wrapped function with authentication and role checks.
        return wrapped_view

    # Returns the decorator so it can be applied to a route.
    return decorator