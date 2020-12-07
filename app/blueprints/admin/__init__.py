from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

admin = Blueprint("admin", __name__, template_folder="templates/admin")


@admin.route("/")
@login_required
def index():
    return redirect(url_for("admin.dashboard"))


@admin.route("/login")
def login():
    return render_template("auth/login.html")


@admin.route("/logout")
def logout():
    return redirect(url_for("admin.login"))


@admin.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@admin.route("/users")
def users():
    return render_template("users/users.html")


@admin.route("/users/edit/")
@admin.route("/users/edit/<user_id>")
def edit_user(user_id=None):
    return render_template("users/user_edit.html")