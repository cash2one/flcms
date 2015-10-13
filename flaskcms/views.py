from flask import Blueprint, render_template


main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder='static', static_url_path='/static')


@main_bp.route('/')
def homepage():
    return render_template("index.html")


@main_bp.errorhandler(404)
def page_not_founded(e):
    return render_template("404.html"), 404


@main_bp.route('/contact/')
def contactpage():
    return render_template("contact.html")