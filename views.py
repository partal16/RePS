from datetime import datetime
from problem import Problem
from student import Student
from authorized_person import AuthorizedPerson
from build import Build

from forms import ProblemAddForm, ProblemEditForm, StudentAddForm
from flask import (
    abort, current_app, redirect, render_template, request, url_for, flash
)
from passlib.hash import pbkdf2_sha256 as hasher
from user import get_user
from flask_login import login_user, logout_user, current_user


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def sign_up_page():
    return render_template("sign_up.html")


def student_add_page():
    if request.method == "GET":
        values = {"first_name": "", "last_name": "", "email": "", "password": ""}
        return render_template("student_edit.html", values=values)
    else:
        f_n = request.form["first_name"]
        l_n = request.form["last_name"]
        e = request.form["email"]
        p = request.form["password"]

        error = None
        db = current_app.config["db"]
        if db.get_student(e) is not None:
            error = "Email {} is already registered.".format(str(e))

        if error is None:
            p = hasher.hash(p)
            student = Student(e, f_n, l_n, p)
            db.add_student(student)
            return redirect(url_for("login_page"))

        flash(error)
        
        values = {"first_name": "", "last_name": "", "email": "", "password": ""}
        return render_template("student_edit.html", values=values)

    
def authorized_add_page():
    if request.method == "GET":
        values = {"first_name": "", "last_name": "", "email": "", "password": ""}
        return render_template("authorized_edit.html", values=values)
    else:
        f_n = request.form["first_name"]
        l_n = request.form["last_name"]
        e = request.form["email"]
        p = request.form["password"]

        error = None
        db = current_app.config["db"]
        if db.get_authorized(e) is not None:
            error = "Email {} is already registered.".format(str(e))

        if error is None:
            p = hasher.hash(p)
            authorized = AuthorizedPerson(e, f_n, l_n, p)
            db.add_authorized(authorized)
            return redirect(url_for("login_page"))

        flash(error)
        value = {"first_name": "", "last_name": "", "email": "", "password": ""}
        return redirect(url_for("login_page"))


def login_page():
    s_id = None
    if request.method == "GET":
        values = {"email": "", "password": ""}
        return render_template("login.html", values=values)
    else:
        email = request.form["email"]
        password = request.form["password"]
        user = get_user(email)
        if user is not None:
            if hasher.verify(password, user.password):
                login_user(user)
                return redirect(url_for("home_page"))
            else:
                flash("Incorrect password")
        else:
            flash("Incorrect email.")

        values = {"email": "", "password": ""}
        return render_template("login.html", values=values)


def logout_page():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home_page"))


def problems_page():
    db = current_app.config["db"]
    if request.method == "GET":
        problems = db.get_problems()
        return render_template("problems.html", problems=sorted(problems))
    else:
        form_problem_keys = request.form.getlist("problem_keys")
        for form_problem_key in form_problem_keys:
            db.delete_problem(int(form_problem_key))
        return redirect(url_for("problems_page"))

def my_problems_page():
    db = current_app.config["db"]
    if request.method == "GET":
        problems = db.get_user_problems(current_user.email, current_user.is_student)
        return render_template("my_problems_page.html", problems=sorted(problems))

    
def problem_delete(problem_key):
    db = current_app.config["db"]
    db.delete_problem(problem_key)
    return redirect(url_for("problems_page"))

def problem_cancel(problem_key):
    db = current_app.config["db"]
    db.cancel_problem(problem_key)
    return redirect(url_for("my_problems_page"))


def problem_page(problem_key):
    db = current_app.config["db"]
    problem = db.get_problem(problem_key)
    if problem is None:
        abort(404)
    return render_template("problem.html", problem=problem)


def problem_add_page():
    form = ProblemAddForm()
    if form.validate_on_submit():
        form_title = request.form["title"]
        form_description = request.form["description"]
        form_build = request.form["build"]
        problem = Problem(form_title, form_description)
        build = Build(form_build)
        db = current_app.config["db"]
        problem_key = db.add_problem(problem, build, current_user.email)
        return redirect(url_for("problem_page", problem_key=problem_key))
    return render_template("problem_add.html", form=form)

def problem_select_page():
    db = current_app.config["db"]
    if request.method == "GET":
        problems = db.get_not_started_problems()
        return render_template("select_problem.html", problems=sorted(problems))

def problem_select(problem_key):
    db = current_app.config["db"]
    db.select_problem(problem_key, current_user.email)
    return redirect(url_for("my_problems_page"))

def problem_edit_page(problem_key):
    db = current_app.config["db"]
    problem = db.get_problem(problem_key)
    form = ProblemEditForm()
    if form.validate_on_submit():
        title = form.data["title"]
        description = form.data["description"]
        problem = Problem(title, description)
        db.update_problem(problem_key, problem)
        return redirect(url_for("problem_page", problem_key=problem_key))
    form.title.data = problem.title
    form.description.data = problem.description
    return render_template("problem_edit.html", form=form,)

