from app.main import main
from app.main.forms import CookiesForm
from flask import (
    current_app,
    flash,
    json,
    make_response,
    redirect,
    render_template,
    request,
)
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import HTTPException


@main.route("", methods=["GET"])
def index():
    return render_template("main/index.html")


@main.route("/cookies", methods=["GET", "POST"])
def cookies():
    form = CookiesForm()
    # Default cookies policy to reject all categories of cookie
    cookies_policy = {"functional": "no"}

    if form.validate_on_submit():
        # Update cookies policy consent from form data
        cookies_policy["functional"] = form.functional.data

        # Create flash message confirmation before rendering template
        flash("You’ve set your cookie preferences.", "success")

        # Create the response so we can set the cookie before returning
        response = make_response(render_template("cookies.html", form=form))

        # Set cookies policy for one year
        response.set_cookie("cookies_policy", json.dumps(cookies_policy), max_age=31557600)
        return response
    elif request.method == "GET":
        if request.cookies.get("cookies_policy"):
            # Set cookie consent radios to current consent
            cookies_policy = json.loads(request.cookies.get("cookies_policy"))
            form.functional.data = cookies_policy["functional"]
        else:
            # If conset not previously set, use default "no" policy
            form.functional.data = cookies_policy["functional"]
    return render_template("cookies.html", form=form)


@main.app_errorhandler(HTTPException)
def http_exception(error):
    current_app.logger.error(f"{error.code}: {error.name} - {request.url}")
    return render_template("error.html", title=error.name, error=error), error.code


@main.app_errorhandler(CSRFError)
def csrf_error(error):
    current_app.logger.error(f"{error.code}: {error.description} - {request.url}")
    flash("The form you were submitting has expired. Please try again.", "info")
    return redirect(request.full_path)
