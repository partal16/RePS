from datetime import datetime

from flask import abort, current_app, render_template

def home_page():
    today = datetime.today()
    day_name = today.strftime("%A")
    return render_template("home.html", day=day_name)


def problems_page():
    db = current_app.config["db"]
    problems = db.get_problems()
    return render_template("problems.html", problems=sorted(problems))

def problem_page(problem_key):
    db = current_app.config["db"]
    problem = db.get_problem(problem_key)
    if problem is None:
        abort(404)
    return render_template("problem.html", problem=problem)
