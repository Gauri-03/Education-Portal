from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Enrollment, Library, Question, Score, Subject, User, db, Educator, Chapter, Quiz

admin = Blueprint("admin", __name__)

@admin.route("/adminhome", methods = ["GET"])
def admin_home():
    educators = Educator.query.all()
    return render_template("admin_home.html", educators = educators)

@admin.route("/adminhome/view_educator/<int:educator_id>", methods = ["GET"])
def view_educator(educator_id):
    subjects = Subject.query.filter_by(educator_id=educator_id).all()
    educator = Educator.query.get(educator_id)
    return render_template("view_educator.html", educator=educator, subjects=subjects)

@admin.route("/adminhome/view_subjects", methods = ["GET"])
def view_subjects():
    subjects = Subject.query.all()
    return render_template("view_subjects.html", subjects = subjects)

@admin.route("/adminhome/update_subject/<int:educator_id>/<int:subject_id>", methods = ["GET", "POST"])
def update_subject(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != subject.name:
            if not updated_name:
                flash("Subject name cannot be empty!", category="error")
                return redirect(url_for("admin.update_subject", subject_id=subject_id))
            if Subject.query.filter_by(name=updated_name).first():
                flash("Subject name already exists!", category="error")
                return redirect(url_for("admin.update_subject", subject_id=subject_id))
            subject.name = updated_name
            db.session.commit()
            flash("Subject name updated successfully!", category="success")
        
        if updated_description != subject.description:
            if not updated_description:
                flash("Subject description cannot be empty!", category="error")
                return redirect(url_for("admin.update_subject", subject_id=subject_id))
            subject.description = updated_description
            db.session.commit()
            flash("Subject description updated successfully!", category="success")

    subjects = Subject.query.filter_by(educator_id=educator_id).all()
    return render_template("view_educator.html",subjects = subjects, educator = educator)

@admin.route("/adminhome/delete_subject/<int:educator_id>/<int:subject_id>", methods = ["POST"])
def delete_subject(educator_id, subject_id):
    if request.method == "POST":
        chapters = Chapter.query.filter_by(subject_id = subject_id)
        for chapter in chapters:
            db.session.delete(chapter)
            db.session.commit()
        quizzes = Quiz.query.filter_by(subject_id = subject_id)
        for quiz in quizzes:
            questions = Question.query.filter_by(quiz_id =quiz.id)
            for question in questions:
                db.session.delete(question)
                db.session.commit()
            db.session.delete(quiz)
            db.session.commit()
        subject = Subject.query.get(subject_id)
        db.session.delete(subject)
        db.session.commit()
        flash("Subject deleted successfully!", category = "success")
    return redirect(url_for("admin.admin_home"))

@admin.route("/adminhome/view_chapter/<int:educator_id>/<int:subject_id>", methods = ["GET"])
def view_chapter(educator_id, subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    return render_template("view_chapters.html",chapters = chapters, educator=educator, subject=subject)

@admin.route("/adminhome/update_chapter/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods = ["GET", "POST"])
def update_chapter(subject_id, educator_id,chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id, subject_id=subject_id).first()
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != chapter.name:
            if not updated_name:
                flash("Chapter name cannot be empty!", category="error")
                return redirect(url_for("admin.update_chapter", chapter_id=chapter_id))
            if Chapter.query.filter_by(name=updated_name).first():
                flash("Chapter name already exists!", category="error")
                return redirect(url_for("admin.update_chapter", chapter_id = chapter_id))
            chapter.name = updated_name
            db.session.commit()
            flash("Chapter name updated successfully!", category="success")
        
        if updated_description != chapter.description:
            if not updated_description:
                flash("Chapter description cannot be empty!", category="error")
                return redirect(url_for("admin.update_chapter", chapter_id = chapter_id))
            chapter.description = updated_description
            db.session.commit()
            flash("Chapter description updated successfully!", category="success")

    chapters = Chapter.query.filter_by(subject_id = subject_id).all()
    return render_template("view_chapters.html",chapters = chapters, educator = educator, subject = subject) 

@admin.route("/adminhome/delete_chapter/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods=["POST"])
def delete_chapter(educator_id, subject_id, chapter_id):
    if request.method == "POST":
        chapter = Chapter.query.get(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", category="success")
    return redirect(url_for("admin.view_chapter", educator_id = educator_id ,subject_id=subject_id))

@admin.route("/adminhome/view_quiz/<int:educator_id>/<int:subject_id>", methods = ["GET"])
def view_quiz(educator_id, subject_id):
    quizzes = Quiz.query.filter_by(subject_id=subject_id).all()
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    return render_template("view_quiz.html", quizzes=quizzes, educator=educator, subject=subject)

@admin.route("/adminhome/update_quiz/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods = ["GET", "POST"])
def update_quiz(subject_id, educator_id,quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, subject_id=subject_id).first()
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != quiz.name:
            if not updated_name:
                flash("Quiz name cannot be empty!", category="error")
                return redirect(url_for("admin.update_chapter", quiz_id = quiz_id))
            if Quiz.query.filter_by(name=updated_name).first():
                flash("Quiz name already exists!", category="error")
                return redirect(url_for("admin.update_quiz", quiz_id = quiz_id))
            quiz.name = updated_name
            db.session.commit()
            flash("Quiz name updated successfully!", category="success")
        
        if updated_description != quiz.description:
            if not updated_description:
                flash("Quiz description cannot be empty!", category="error")
                return redirect(url_for("admin.update_chapter", quiz_id = quiz_id))
            quiz.description = updated_description
            db.session.commit()
            flash("Quiz description updated successfully!", category="success")

    quizzes = Quiz.query.filter_by(subject_id = subject_id).all()
    return render_template("view_quiz.html",quizzes = quizzes, educator = educator, subject = subject) 

@admin.route("/adminhome/delete_quiz/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods=["POST"])
def delete_quiz(educator_id, subject_id, quiz_id):
    if request.method == "POST":
        questions = Question.query.filter_by(quiz_id = quiz_id)
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        quiz = Quiz.query.get(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted successfully!", category="success")
    return redirect(url_for("admin.view_quiz", educator_id = educator_id ,subject_id=subject_id))


@admin.route("/adminhome/view_content/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods = ["GET"])
def view_content(educator_id, subject_id, chapter_id):
    educator = Educator.query.get(educator_id)
    subject =Subject.query.get(subject_id)
    chapter = Chapter.query.get(chapter_id)

    content = chapter.content
    return render_template("view_content.html", educator=educator, subject=subject, chapter=chapter, content=content)

@admin.route("/adminhome/update_content/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods = ["GET", "POST"])
def update_content(educator_id, subject_id, chapter_id):
    educator = Educator.query.get(educator_id)
    subject =Subject.query.get(subject_id)
    chapter = Chapter.query.get(chapter_id)

    if request.method == "POST":
        updated_content = request.form.get("content")

        if updated_content != chapter.content:
            if not updated_content:
                flash("Content canot be empty", category= "error")
                return redirect(url_for("admin.update_content", educator_id = educator_id, subject_id = subject_id, chapter_id = chapter_id))
            if Chapter.query.filter_by(content = updated_content).first():
                flash("Chapter content already exists!", category="error")
                return redirect(url_for("admin.update_content", educator_id = educator_id, subject_id = subject_id, chapter_id = chapter_id))
            chapter.content = updated_content
            db.session.commit()
            flash("Content updated successfully!", category= "success")
        
        content = chapter.content

    return render_template("view_content.html", educator = educator, subject = subject, chapter = chapter, content = content)

@admin.route("/adminhome/view_questions/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods = ["GET"])
def view_questions(educator_id, subject_id, quiz_id):
    educator = Educator.query.get(educator_id)
    subject =Subject.query.get(subject_id)
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id = quiz_id)
    return render_template("view_questions.html", educator = educator, subject = subject, quiz = quiz, questions = questions)

@admin.route("/adminhome/update_question/<int:educator_id>/<int:subject_id>/<int:quiz_id>/<int:question_id>", methods = ["GET", "POST"])
def update_questions(educator_id, subject_id, quiz_id, question_id):
    question = Question.query.filter_by(id = question_id).first()
    quiz = Quiz.query.get(quiz_id)
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)

    if request.method == "POST":
        updated_statement = request.form.get("statement")
        updated_option_a = request.form.get("optiona")
        updated_option_b = request.form.get("optionb")
        updated_option_c = request.form.get("optionc")
        updated_option_d = request.form.get("optiond")
        all_options = [updated_option_a, updated_option_b, updated_option_c, updated_option_d]
        updated_correct_answer = request.form.get("correct_answer")
        
        if updated_statement != question.statement:
            if not updated_statement:
                flash("Statement required!", category = "error")
                return redirect(url_for("admin.update_question", subject_id = subject_id, quiz_id = quiz_id, question_id = question_id, educator_id=educator_id))
            if Question.query.filter_by(statement = updated_statement).first():
                flash("Question already exists!", category = "error")
                return redirect(url_for("admin.update_question", subject_id = subject_id, quiz_id = quiz_id, question_id = question_id, educator_id=educator_id))
            question.statement = updated_statement
            db.session.commit()
            flash("Question statement updated successfully!", category = "success")
        if updated_correct_answer not in all_options:
            flash("Correct answer must be one of the provided options!", category="error")
            return redirect(url_for("admin.update_question", subject_id=subject_id, quiz_id=quiz_id, question_id=question_id, educator_id=educator_id))
        if updated_option_a != question.option_a:
            question.option_a = updated_option_a
            db.session.commit()
            flash("Option A updated successfully!", category = "success")
        if updated_option_b != question.option_b:
            question.option_b = updated_option_b
            db.session.commit()
            flash("Option B updated successfully!", category = "success")
        if updated_option_c != question.option_c:
            question.option_c = updated_option_c
            db.session.commit()
            flash("Option C updated successfully!", category = "success")
        if updated_option_d != question.option_d:
            question.option_d = updated_option_d
            db.session.commit()
            flash("Option D updated successfully!", category = "success")
        if updated_correct_answer != question.correct_answer:
            question.correct_answer = updated_correct_answer
            db.session.commit()
            flash("Correct answer updated successfully!", category = "success")
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template("view_questions.html", subject = subject, educator = educator, quiz = quiz, question = question, questions = questions)

@admin.route("/adminhome/delete_question/<int:educator_id>/<int:subject_id>/<int:quiz_id>/<int:question_id>", methods=["POST"])
def delete_question(educator_id, subject_id, quiz_id, question_id):
    if request.method == "POST":
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            flash("Question deleted successfully!", category="success")
        else:
            flash("Question not found!", category="error")
    return redirect(url_for("admin.view_questions", educator_id = educator_id ,subject_id=subject_id, quiz_id=quiz_id))

@admin.route("/adminhome/search", methods = ["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search")
        search_type = request.form.get("search_type")

        if search_type == "user":
            users = User.query.filter(User.username.ilike(f"%{search_term}%")).all()
            if not users:
                flash(f"No users found matching '{search_term}'", category = "error")
                return render_template("search_admin.html")
            return render_template("view_users.html", users = users, search_term = search_term)
        elif search_type == "educator":
            educators = Educator.query.filter(Educator.username.ilike(f"%{search_term}%")).all()
            if not educators:
                flash(f"No educators found matching '{search_term}'", category = "error")
                return render_template("search_admin.html")
            return render_template("admin_home.html", educators = educators, search_term = search_term)
    return render_template("search_admin.html")

@admin.route("/adminhome/view_users", methods=["GET", "POST"])
def view_users():
    users = User.query.all()
    return render_template("view_users.html", users=users)

@admin.route("/adminhome/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if request.method == "POST":
        user = User.query.get(user_id)
        if user:
            # First, delete all related enrollment records
            db.session.query(Enrollment).filter(Enrollment.user_id == user_id).delete()
            db.session.query(Library).filter(Library.user_id == user_id).delete()
            db.session.query(Score).filter(Score.user_id == user_id).delete()
            # Now, delete the user
            db.session.delete(user)
            db.session.commit()
            flash("User deleted successfully!", category="success")
        else:
            flash("User not found!", category="error")
    return redirect(url_for("admin.view_users"))
