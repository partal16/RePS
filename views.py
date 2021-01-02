from datetime import datetime
from problem import Problem
from forms import ProblemAddForm, ProblemEditForm
from flask import abort, current_app, redirect,render_template, request, url_for


def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


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

    
def problem_delete(problem_key):
    db = current_app.config["db"]
    db.delete_problem(problem_key)
    return redirect(url_for("problems_page"))


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
        db = current_app.config["db"]
        problem_key = db.add_problem(problem)
        return redirect(url_for("problem_page", problem_key=problem_key))
    return render_template("problem_add.html", form=form)


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

