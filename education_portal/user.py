from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import Chapter, Enrollment, Library, Question, Quiz, Score, Subject, User, db

user = Blueprint("user", __name__)

@user.route("/userhome/<int:user_id>", methods = ["GET"])
def user_home(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found!", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))
    subjects = Subject.query.all()
    return render_template("user_home.html", subjects = subjects, user = user, user_id = user_id)


@user.route("/userhome/enroll/<int:user_id>/<int:subject_id>", methods=["POST"])
def enroll_in_subject(user_id, subject_id):
    user = User.query.get(user_id)
    subject = Subject.query.get(subject_id)
    
    if not user or not subject:
        flash("User or Subject not found.", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))

    existing_enrollment = Enrollment.query.filter_by(user_id=user.id, subject_id=subject.id).first()
    if existing_enrollment:
        flash("You are already enrolled in this subject.", category="info")
        return redirect(url_for("user.user_home", user_id=user.id))

    new_enrollment = Enrollment(user_id=user.id, subject_id=subject.id)
    db.session.add(new_enrollment)
    db.session.commit()

    flash("Successfully enrolled in the subject!", category="success")
    return redirect(url_for("user.user_home", user_id=user.id))

@user.route("/userhome/my_subjects/<int:user_id>", methods=["GET"])
def my_subjects(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found!", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))

    enrollments = Enrollment.query.filter_by(user_id=user.id).all()
    subjects = [enrollment.subject for enrollment in enrollments]

    return render_template("my_subjects_user.html", subjects=subjects, user=user, user_id=user_id)

@user.route("/userhome/view_chapters/<int:user_id>/<int:subject_id>", methods=["GET"])
def view_chapters_user(user_id, subject_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found!", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))

    subject = Subject.query.get(subject_id)
    if not subject:
        flash("Subject not found!", category="error")
        return redirect(url_for("user.user_home", user_id=user.id))

    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    return render_template("view_chapters_user.html", chapters=chapters, user=user, subject=subject, user_id=user_id)

@user.route("/userhome/view_chapter_content/<int:user_id>/<int:chapter_id>", methods=["GET"])
def view_chapter_content_user(user_id, chapter_id):
    user = User.query.get(user_id)
    chapter = Chapter.query.get(chapter_id)

    content = chapter.content
    return render_template("view_content_user.html", user = user, chapter=chapter, content=content)

@user.route("/userhome/view_quiz/<int:user_id>/<int:subject_id>", methods = ["GET"])
def view_quiz_user(subject_id, user_id):
    user = User.query.get(user_id)
    quizzes = Quiz.query.filter_by(subject_id = subject_id).all() 
    subject = Subject.query.get(subject_id)
    return render_template("view_quiz_user.html", quizzes = quizzes, subject = subject, user = user)

@user.route("/userhome/view_questions/<int:user_id>/<int:subject_id>/<int:quiz_id>", methods=["GET", "POST"])
def view_questions_user(subject_id, quiz_id, user_id):
    user = User.query.get(user_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz = Quiz.query.get(quiz_id)
    subject = Subject.query.get(subject_id)
    return render_template("view_questions_user.html", questions=questions, quiz=quiz, subject=subject, user=user)


@user.route('/userhome/submit_quiz/<int:user_id>/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id, user_id):
    user = User.query.get(user_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    score = 0
    for question in questions:
        user_answer = request.form.get(f'question_{question.id}')
        if user_answer and user_answer == question.correct_answer:
            score += 1
    new_score = Score(user_id = user_id, quiz_id=quiz_id, marks=score)
    db.session.add(new_score)
    db.session.commit()
    return redirect(url_for("user.quiz_results", quiz_id=quiz_id, user =user, user_id=user_id))

@user.route("/userhome/results/<int:user_id>/quiz/<int:quiz_id>", methods = ["GET"])
def quiz_results(user_id,quiz_id):
    user = User.query.get(user_id)
    quiz = Quiz.query.get(quiz_id)
    user_scores = Score.query.filter_by(user_id = user_id, quiz_id=quiz_id).order_by(Score.id.desc()).all()
    remaining_scores = user_scores[1:]
    latest_score = user_scores[0]
    return render_template("quiz_results.html", quiz=quiz, user_scores=user_scores, user =user, latest_score=latest_score, remaining_scores=remaining_scores)

    
@user.route("/userhome/add_to_library/<int:user_id>/<int:chapter_id>", methods=["POST"])
def add_to_library(user_id, chapter_id):
    user = User.query.get(user_id)
    chapter = Chapter.query.get(chapter_id)
    if not user or not chapter:
        flash("User or Chapter not found.", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))
    existing_entry = Library.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()
    if existing_entry:
        flash("Chapter already saved to your library.", category="info")
        return redirect(url_for("user.user_home", user_id=user_id))
    new_entry = Library(user_id=user_id, chapter_id=chapter_id)
    db.session.add(new_entry)
    db.session.commit()
    flash("Chapter added to your library!", category="success")
    subject_id = chapter.subject_id
    return redirect(url_for("user.view_chapters_user", user_id=user_id, subject_id = subject_id))

@user.route("/userhome/library/<int:user_id>")
def view_library(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", category="error")
        return redirect(url_for("user.user_home", user_id=user_id))
    
    library_items = Library.query.filter_by(user_id=user_id).all()
    
    saved_chapters = [Chapter.query.get(item.chapter_id) for item in library_items]

    return render_template("library.html", saved_chapters=saved_chapters, user=user, user_id=user_id)


@user.route("/library/remove/<int:user_id>/<int:chapter_id>", methods=["POST"])
def remove_from_library(user_id, chapter_id):
    entry = Library.query.filter_by(user_id=user_id, chapter_id=chapter_id).first()

    if entry:
        db.session.delete(entry)
        db.session.commit()
        flash("Chapter removed from your library.", category="success")
    else:
        flash("Chapter not found in your library.", category="error")

    return redirect(url_for("user.view_library", user_id=user_id))
