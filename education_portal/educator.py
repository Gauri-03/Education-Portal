from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import Chapter, Educator, Question, Quiz, Subject, db

educator = Blueprint("educator", __name__)

@educator.route("/educatorhome/<int:educator_id>", methods=["GET", "POST"])
def educator_home(educator_id):
    educator = Educator.query.get(educator_id)
    subjects = Subject.query.filter_by(educator_id=educator.id).all()
    return render_template("educator_home.html", educator_id=educator_id, subjects=subjects, educator=educator)


@educator.route("/educatorhome/create_subject/<int:educator_id>", methods=["GET", "POST"])
def create_subject(educator_id):
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        form_name = request.form.get("name")
        form_description = request.form.get("description")

        subject = Subject.query.filter_by(name=form_name).first()
        if subject:
            flash("Subject already exists!", category="error")
            return redirect(url_for("educator.create_subject", educator_id=educator_id))

        new_subject = Subject(name=form_name, description=form_description, educator_id=educator_id)
        db.session.add(new_subject)
        db.session.commit()
        flash("Subject created successfully!", category="success")
        return redirect(url_for("educator.educator_home", educator = educator, educator_id=educator_id))
    subjects = Subject.query.filter_by(educator_id=educator_id).all()
    return render_template("educator_home.html", educator_id=educator_id, subjects=subjects, educator=educator)

@educator.route("/educatorhome/update_subject_edu/<int:educator_id>/<int:subject_id>", methods = ["GET", "POST"])
def update_subject_edu(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != subject.name:
            if not updated_name:
                flash("Subject name cannot be empty!", category="error")
                return redirect(url_for("educator.update_subject_edu", subject_id=subject_id, educator_id=educator_id))
            if Subject.query.filter_by(name=updated_name).first():
                flash("Subject name already exists!", category="error")
                return redirect(url_for("educator.update_subject_edu", subject_id=subject_id, educator_id=educator_id))
            subject.name = updated_name
            db.session.commit()
            flash("Subject name updated successfully!", category="success")
        
        if updated_description != subject.description:
            if not updated_description:
                flash("Subject description cannot be empty!", category="error")
                return redirect(url_for("educator.update_subject_edu", subject_id=subject_id, educator_id=educator_id))
            subject.description = updated_description
            db.session.commit()
            flash("Subject description updated successfully!", category="success")

    subjects = Subject.query.filter_by(educator_id=educator_id).all()
    return render_template("educator_home.html",subjects = subjects, educator = educator, educator_id = educator_id)

@educator.route("/educatorhome/delete_subject_edu/<int:educator_id>/<int:subject_id>", methods = ["POST"])
def delete_subject_edu(educator_id, subject_id):
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
    return redirect(url_for("educator.educator_home", subject_id = subject_id, educator_id = educator_id))

@educator.route("/educatorhome/view_chapters_edu/<int:educator_id>/<int:subject_id>", methods=["GET", "POST"])
def view_chapters_edu(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    return render_template("view_chapters_edu.html", subject=subject, educator=educator, chapters=chapters)

@educator.route("/educatorhome/create_chapters_edu/<int:educator_id>/<int:subject_id>", methods=["GET", "POST"])
def create_chapters_edu(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        form_name = request.form.get("name")
        form_description = request.form.get("description")
        form_content = request.form.get("content")
        if Chapter.query.filter_by(name = form_name).first():
            flash("Chapter already exists!", category = "error")
            return redirect(url_for("educator.view_chapters_edu", educator_id = educator_id ,subject_id = subject_id))
        else:
            new_chapter = Chapter(name = form_name, description = form_description, content = form_content, subject_id = subject_id)
            db.session.add(new_chapter)
            db.session.commit()
            flash("Chapter added successfully!", category = "success")
            return redirect(url_for("educator.view_chapters_edu", educator_id = educator_id ,subject_id = subject_id))
    return render_template("view_chapters_edu.html", subject=subject, educator=educator)

@educator.route("/educatorhome/update_chapter_edu/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods=["GET", "POST"])
def update_chapter_edu(chapter_id, subject_id, educator_id):
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != chapter.name:
            if not updated_name:
                flash("Chapter name cannot be empty!", category="error")
                return redirect(url_for("educator.update_chapter_edu", chapter_id=chapter_id, subject_id=subject_id, educator_id=educator_id))
            if Chapter.query.filter_by(name=updated_name).first():
                flash("Chapter name already exists!", category="error")
                return redirect(url_for("educator.update_chapter_edu", chapter_id=chapter_id, subject_id=subject_id, educator_id=educator_id))
            chapter.name = updated_name
            db.session.commit()
            flash("Chapter name updated successfully!", category="success")
        
        if updated_description != chapter.description:
            if not updated_description:
                flash("Chapter description cannot be empty!", category="error")
                return redirect(url_for("educator.update_chapter_edu", chapter_id=chapter_id, subject_id=subject_id, educator_id=educator_id))
            chapter.description = updated_description
            db.session.commit()
            flash("Chapter description updated successfully!", category="success")

    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    return render_template("view_chapters_edu.html", chapters=chapters, subject=subject, educator=educator)

@educator.route("/educatorhome/delete_chapter/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods=["POST"])
def delete_chapter_edu(educator_id, subject_id, chapter_id):
    if request.method == "POST":
        chapter = Chapter.query.get(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        flash("Chapter deleted successfully!", category="success")
    return redirect(url_for("educator.view_chapters_edu", educator_id = educator_id ,subject_id=subject_id))

@educator.route("/educatorhome/view_content_edu/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods=["GET", "POST"])
def view_content_edu(chapter_id, subject_id, educator_id):
    chapter = Chapter.query.get(chapter_id)
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    content = chapter.content
    return render_template("view_content_edu.html", chapter=chapter, subject=subject, educator=educator, content=content)

@educator.route("/educatorhome/update_content_edu/<int:educator_id>/<int:subject_id>/<int:chapter_id>", methods = ["GET", "POST"])
def update_content_edu(educator_id, subject_id, chapter_id):
    educator = Educator.query.get(educator_id)
    subject = Subject.query.get(subject_id)
    chapter = Chapter.query.get(chapter_id)

    if request.method == "POST":
        updated_content = request.form.get("content")

        if updated_content != chapter.content:
            if not updated_content:
                flash("Content canot be empty", category= "error")
                return redirect(url_for("educator.update_content_edu", educator_id = educator_id, subject_id = subject_id, chapter_id = chapter_id))
            if Chapter.query.filter_by(content = updated_content).first():
                flash("Chapter content already exists!", category="error")
                return redirect(url_for("educator.update_content_edu", educator_id = educator_id, subject_id = subject_id, chapter_id = chapter_id))
            chapter.content = updated_content
            db.session.commit()
            flash("Content updated successfully!", category= "success")
        
        content = chapter.content

    return render_template("view_content_edu.html", educator = educator, subject = subject, chapter = chapter, content = content)

@educator.route("/educatorhome/view_quizzes_edu/<int:educator_id>/<int:subject_id>", methods=["GET", "POST"])
def view_quizzes_edu(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    quizzes = Quiz.query.filter_by(subject_id=subject.id).all()
    return render_template("view_quizzes_edu.html", subject=subject, educator=educator, quizzes=quizzes)

@educator.route("/educatorhome/create_quizzes_edu/<int:educator_id>/<int:subject_id>", methods=["GET", "POST"])
def create_quizzes_edu(subject_id, educator_id):
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        form_name = request.form.get("name")
        form_description = request.form.get("description")
        if Quiz.query.filter_by(name = form_name).first():
            flash("Quiz already exists!", category = "error")
            return redirect(url_for("educator.view_quizzes_edu", educator_id = educator_id ,subject_id = subject_id))
        else:
            new_quiz = Quiz(name = form_name, description = form_description, subject_id = subject_id)
            db.session.add(new_quiz)
            db.session.commit()
            flash("Quiz added successfully!", category = "success")
            return redirect(url_for("educator.view_quizzes_edu", educator_id = educator_id ,subject_id = subject_id))
    return render_template("view_quizzes_edu.html", subject=subject, educator=educator)

@educator.route("/educatorhome/update_quizzes_edu/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods = ["GET", "POST"])
def update_quizzes_edu(subject_id, educator_id,quiz_id):
    quiz = Quiz.query.filter_by(id=quiz_id, subject_id=subject_id).first()
    subject = Subject.query.get(subject_id)
    educator = Educator.query.get(educator_id)
    if request.method == "POST":
        updated_name = request.form.get("name")
        updated_description = request.form.get("description")

        if updated_name != quiz.name:
            if not updated_name:
                flash("Quiz name cannot be empty!", category="error")
                return redirect(url_for("educator.update_quizzes_edu", quiz_id = quiz_id))
            if Quiz.query.filter_by(name=updated_name).first():
                flash("Quiz name already exists!", category="error")
                return redirect(url_for("educator.update_quizzes_edu", quiz_id = quiz_id))
            quiz.name = updated_name
            db.session.commit()
            flash("Quiz name updated successfully!", category="success")
        
        if updated_description != quiz.description:
            if not updated_description:
                flash("Quiz description cannot be empty!", category="error")
                return redirect(url_for("educator.update_quizzes_edu", quiz_id = quiz_id))
            quiz.description = updated_description
            db.session.commit()
            flash("Quiz description updated successfully!", category="success")

    quizzes = Quiz.query.filter_by(subject_id = subject_id).all()
    return render_template("view_quizzes_edu.html",quizzes = quizzes, educator = educator, subject = subject) 

@educator.route("/educatorhome/delete_quiz/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods=["POST"])
def delete_quiz_edu(educator_id, subject_id, quiz_id):
    if request.method == "POST":
        questions = Question.query.filter_by(quiz_id = quiz_id)
        for question in questions:
            db.session.delete(question)
            db.session.commit()
        quiz = Quiz.query.get(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        flash("Quiz deleted successfully!", category="success")
    return redirect(url_for("educator.view_quizzes_edu", educator_id = educator_id ,subject_id=subject_id))

@educator.route("/educatorhome/view_questions_edu/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods = ["GET"])
def view_questions_edu(educator_id, subject_id, quiz_id):
    educator = Educator.query.get(educator_id)
    subject =Subject.query.get(subject_id)
    quiz = Quiz.query.get(quiz_id)
    questions = Question.query.filter_by(quiz_id = quiz_id)
    return render_template("view_questions_edu.html", educator = educator, subject = subject, quiz = quiz, questions = questions)

@educator.route("/educatorhome/create_questions_edu/<int:educator_id>/<int:subject_id>/<int:quiz_id>", methods = ["GET", "POST"])
def create_questions_edu(educator_id, subject_id, quiz_id):
    educator = Educator.query.get(educator_id)
    subject = Subject.query.get(subject_id)
    quiz = Quiz.query.get(quiz_id)
    if request.method == "POST":
    
        statement = request.form.get("statement")
        option_a = request.form.get("optiona")
        option_b = request.form.get("optionb")
        option_c = request.form.get("optionc")
        option_d = request.form.get("optiond")
        correct_answer = request.form.get("correct_answer")
        
        all_options = [option_a, option_b, option_c, option_d]
        
        if Question.query.filter_by(statement=statement).first():
            flash("Question already exists!", category="error")
            return redirect(url_for("educator.view_questions_edu", educator_id = educator_id,subject_id=subject_id, quiz_id=quiz_id))
        
        if correct_answer not in all_options:
            flash("Correct answer must be one of the provided options!", category="error")
            return redirect(url_for("educator.view_questions_edu", educator_id = educator_id, subject_id=subject_id, quiz_id=quiz_id))
        
        new_question = Question(statement=statement, option_a=option_a, option_b=option_b, option_c=option_c, option_d=option_d, correct_answer=correct_answer, quiz_id=quiz_id)
        db.session.add(new_question)
        db.session.commit()
        flash("Question added successfully!", category="success")
        return redirect(url_for("educator.view_questions_edu", educator_id = educator_id, subject_id=subject_id, quiz_id=quiz_id))
    
    return render_template("view_questions_edu.html", educator=educator, subject=subject, quiz=quiz)

@educator.route("/educatorhome/update_questions_edu/<int:educator_id>/<int:subject_id>/<int:quiz_id>/<int:question_id>", methods = ["GET", "POST"])
def update_questions_edu(educator_id, subject_id, quiz_id, question_id):
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
                return redirect(url_for("educator.update_questions_edu", subject_id = subject_id, quiz_id = quiz_id, question_id = question_id, educator_id=educator_id))
            if Question.query.filter_by(statement = updated_statement).first():
                flash("Question already exists!", category = "error")
                return redirect(url_for("educator.update_questions_edu", subject_id = subject_id, quiz_id = quiz_id, question_id = question_id, educator_id=educator_id))
            question.statement = updated_statement
            db.session.commit()
            flash("Question statement updated successfully!", category = "success")
        if updated_correct_answer not in all_options:
            flash("Correct answer must be one of the provided options!", category="error")
            return redirect(url_for("educator.update_questions_edu", subject_id=subject_id, quiz_id=quiz_id, question_id=question_id, educator_id=educator_id))
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
    return render_template("view_questions_edu.html", subject = subject, educator = educator, quiz = quiz, question = question, questions = questions)

@educator.route("/educatorhome/delete_question/<int:educator_id>/<int:subject_id>/<int:quiz_id>/<int:question_id>", methods=["POST"])
def delete_question_edu(educator_id, subject_id, quiz_id, question_id):
    if request.method == "POST":
        question = Question.query.get(question_id)
        if question:
            db.session.delete(question)
            db.session.commit()
            flash("Question deleted successfully!", category="success")
        else:
            flash("Question not found!", category="error")
    return redirect(url_for("educator.view_questions_edu", educator_id = educator_id ,subject_id=subject_id, quiz_id=quiz_id))


@educator.route("/educatorhome/search/<int:educator_id>", methods=["GET", "POST"])
def edu_search(educator_id):
    educator = Educator.query.get(educator_id)
    subjects = []
    search_term = ""

    if request.method == "POST":
        search_term = request.form.get("search")
        subjects = Subject.query.filter(
            Subject.name.ilike(f"%{search_term}%"),
            Subject.educator_id == educator_id 
        ).all()

        if subjects:
            return render_template("educator_home.html", educator=educator, subjects=subjects, search_term=search_term, educator_id=educator_id)
        else:
            flash(f"No subjects found matching '{search_term}'", category="error")

    return render_template("search_educator.html", educator=educator, subjects=subjects, search_term=search_term)
