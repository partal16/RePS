from flask import Flask
from flask_login import LoginManager

import views
from database import Database
from problem import Problem
from user import get_user

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")

    app.add_url_rule("/", view_func=views.home_page, methods=["GET", "POST"],)
    app.add_url_rule("/<int:problem_key>/increase", view_func=views.seen_increase,
                     methods=["GET","POST"],)
    app.add_url_rule("/signup", view_func=views.sign_up_page, methods=["GET", "POST"],)
    app.add_url_rule("/login", view_func=views.login_page, methods=["GET", "POST"],)
    app.add_url_rule("/logout", view_func=views.logout_page)
    app.add_url_rule("/profile", view_func=views.profile_page,
                     methods=["GET", "POST"])
    app.add_url_rule("/profile/<int:user_id>/delete", view_func=views.user_delete,
                     methods=["GET", "POST"])
    app.add_url_rule("/problems", view_func=views.problems_page, methods=["GET", "POST"],)
    app.add_url_rule("/my-problems", view_func=views.my_problems_page, methods=["GET", "POST"],)
    app.add_url_rule("/no-selected-problems", view_func=views.problem_select_page,
                     methods=["GET", "POST"],)
    app.add_url_rule("/no-selected-problems/<int:problem_key>/select",
                     view_func=views.problem_select,
                     methods=["GET", "POST"],)
    app.add_url_rule("/problems/<int:problem_key>", view_func=views.problem_page)
    app.add_url_rule("/problems/<int:problem_key>/delete",
                     view_func=views.problem_delete,
                     methods=["GET", "POST"],)
    app.add_url_rule("/problems/<int:problem_key>/edit",
                     view_func=views.problem_edit_page,
                     methods=["GET", "POST"],)
    app.add_url_rule("/my-problems/<int:problem_key>", view_func=views.problem_page)
    app.add_url_rule("/my-problems/<int:problem_key>/delete",
                     view_func=views.problem_delete,
                     methods=["GET", "POST"],)
    app.add_url_rule("/my-problems/<int:problem_key>/edit",
                     view_func=views.problem_edit_page,
                     methods=["GET", "POST"],)
    app.add_url_rule("/my-problems/<int:problem_key>/cancel",
                     view_func=views.problem_cancel,
                     methods=["GET", "POST"],)
    app.add_url_rule("/my-problems/<int:problem_key>/finish",
                     view_func=views.problem_finish,
                     methods=["GET", "POST"],)
    
    app.add_url_rule("/new-problem", view_func=views.problem_add_page, methods=["GET", "POST"])
    app.add_url_rule("/new-student", view_func=views.student_add_page, methods=["GET", "POST"],)
    app.add_url_rule("/new-authorized", view_func=views.authorized_add_page,
                     methods=["GET", "POST"],)
    app.add_url_rule("/new-password", view_func=views.new_password_page,
                     methods=["GET", "POST"],)

    lm.init_app(app)
    lm.login_view = "login_page"
    
    db = Database('database.ini')
    app.config["db"] = db


    return app


if __name__ == "__main__":
    app = create_app()
    port = app.config.get("PORT", 5000)
    app.run(host="0.0.0.0", port=port)
