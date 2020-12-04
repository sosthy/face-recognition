from flask import Blueprint

frontoffice = Blueprint(
    "frontoffice", __name__, template_folder="templates", static_folder="static"
)
