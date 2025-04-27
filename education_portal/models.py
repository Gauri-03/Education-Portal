from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "educationportal.db"

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password 

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    qualification = db.Column(db.Text, nullable = False)
    dob = db.Column(db.Date)
    score= db.relationship('Score', backref = 'user')
    enrollment = db.relationship('Enrollment', backref='user')

class Educator(db.Model):
    __tablename__ = "educator"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    username = db.Column(db.Text, unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    qualification = db.Column(db.Text, nullable = False)
    fullname = db.Column(db.Text, nullable = False) 
    subject = db.relationship('Subject', backref = 'educator')

class Subject(db.Model):
    __tablename__ = "subject"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    quiz = db.relationship('Quiz', backref = 'subject')
    chapter = db.relationship('Chapter', backref = 'subject')
    educator_id = db.Column(db.Integer, db.ForeignKey("educator.id"), nullable=False)
    enrollment = db.relationship('Enrollment', backref='subject')

class Chapter(db.Model):
    __tablename__ = "chapter"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)


class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    question = db.relationship('Question', backref = 'quiz')
    score = db.relationship('Score', backref = 'quiz')
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    statement = db.Column(db.Text, nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False) 
    option_a = db.Column(db.Text, nullable = False)
    option_b = db.Column(db.Text, nullable = False)
    option_c = db.Column(db.Text, nullable = False)
    option_d = db.Column(db.Text, nullable = False)
    correct_answer = db.Column(db.Text, nullable = False)

class Score(db.Model):
    __tablename__ = "score"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) 
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False) 
    marks = db.Column(db.Integer, nullable=False)  

class Enrollment(db.Model):
    __tablename__ = "enrollment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)

    def __init__(self, user_id, subject_id):
        self.user_id = user_id
        self.subject_id = subject_id

class Library(db.Model):
    __tablename__ = "library"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    user = db.relationship('User', backref='library')
    chapter = db.relationship('Chapter')

    def __init__(self, user_id, chapter_id):
        self.user_id = user_id
        self.chapter_id = chapter_id
