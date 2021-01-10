from flask_login import UserMixin
from flask import current_app

class User(UserMixin):
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.id = email
        self.active = True
        self.is_student = True

        @property
        def is_active(self):
            return self.active

def get_user(user_id):
    db = current_app.config["db"]
    u_in = db.get_student(user_id)
    if u_in == None:
        u_in = db.get_authorized(user_id)
        if u_in == None:
            return None
        else:
            p = u_in[2]
            user = User(user_id, p)
            user.is_student = False
    else:
        p = u_in[2]
        user = User(user_id, p)
    return user
