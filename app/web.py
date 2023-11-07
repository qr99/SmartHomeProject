from flask import Blueprint, send_from_directory, render_template


web_blueprint = Blueprint("web", __name__)


@web_blueprint.route("/<path:path>", methods=["GET"])
def get_path(path):
    """serving static file for the webapp"""
    return send_from_directory("webapp", path)


@web_blueprint.route("/", methods=["GET"])
def get_root():
    """returns the main application page"""
    return render_template("espresso_automat.html")
