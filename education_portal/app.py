from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from os import path
from models import db, DB_NAME
from auth import auth
from admin import admin
from stats import stats
from educator import educator
from user import user
from utils import users, educators, subjects, chapters, quizzes, questions

bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'finalyearproj'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

db.init_app(app)
bcrypt.init_app(app)

def add_admin():
    from models import Admin
    username = "admin"
    password = "admin"
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    admin = Admin(username=username, password=hashed_password)

    db.session.add(admin)
    db.session.commit()

with app.app_context():
    if not path.exists('./instance/' + DB_NAME):
        print("Creating DB")
        db.create_all()
        print("DB created successfully")
        add_admin()
        print("Admin added successfully")

        db.session.add_all(users)
        db.session.add_all(educators)
        db.session.add_all(subjects)
        db.session.add_all(chapters)
        db.session.add_all(quizzes)
        db.session.add_all(questions)
        db.session.commit()
        

app.register_blueprint(auth, url_prefix = "/")
app.register_blueprint(admin, url_prefix = "/")
app.register_blueprint(stats, url_prefix = "/")
app.register_blueprint(user, url_prefix = "/")
app.register_blueprint(educator, url_prefix = "/")

if __name__ == '__main__':
    app.run(debug=True)
