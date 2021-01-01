from flask import Flask

import views
from database import Database
from problem import Problem

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page)
    app.add_url_rule("/problems", view_func=views.problems_page, methods=["GET", "POST"])
    app.add_url_rule("/problems/<int:problem_key>", view_func=views.problem_page)
    app.add_url_rule("/problems/<int:problem_key>/delete",
                     view_func=views.problem_delete,
                     methods=["GET", "POST"],)
    app.add_url_rule("/problems/<int:problem_key>/edit",
                     view_func=views.problem_edit_page,
                     methods=["GET", "POST"],)
    app.add_url_rule("/problems/<int:problem_key>/editn",
                     view_func=views.problem_edit_page,
                     methods=["GET", "POST"],)

    app.add_url_rule("/new-problem", view_func=views.problem_add_page, methods=["GET", "POST"])

    db = Database()
    app.config["db"] = db

    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
