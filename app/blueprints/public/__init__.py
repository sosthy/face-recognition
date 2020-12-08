from flask import Blueprint, render_template

public = Blueprint("public", __name__, template_folder="templates")

from . import events


@public.route("/")
def home():
    return render_template("public/index.html")
