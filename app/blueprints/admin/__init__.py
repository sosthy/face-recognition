from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from app.models import User
from app import bcrypt

db = SQLAlchemy()

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
    users = User.query.all()
    return render_template("users/users.html", users=users)


@admin.route("/users/edit/", methods=["GET", "POST"])
@admin.route("/users/edit/<user_id>", methods=["GET", "POST"])
def edit_user(user_id=None):
    if request.method == "POST":
        user = User()
        user.login = request.form["login"]
        user.firstname = request.form["firstname"]
        user.lastname = request.form["lastname"]
        user.email = request.form["email"]
        user.phone = request.form["phone"]
        user.role = request.form["role"]
        user.password = bcrypt.generate_password_hash("********")

        if "photo" in request.files:
            file = request.files["photo"]
            filename = secure_filename(file.filename)
            file.save(
                os.path.join(
                    current_app.root_path, current_app.config["UPLOAD_FOLDER"], filename
                )
            )
            user.photo = filename
        else:
            flash("No photo selected")
            return redirect(url_for(request.url))

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("admin.users"))
    return render_template("users/user_edit.html")