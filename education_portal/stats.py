from flask import Blueprint, flash, redirect, render_template, url_for
from models import Enrollment, Library, User, Educator, Subject, Chapter, Quiz, Score, db
from sqlalchemy.sql import func

stats = Blueprint("stats", __name__)

@stats.route("/adminhome/user_stats/<int:user_id>")
def user_stats(user_id):
    user = User.query.get(user_id)

    user_scores = Score.query.filter_by(user_id=user_id).all()

    total_quizzes_attempted = len(user_scores)
    total_chapters_saved = Library.query.filter_by(user_id=user_id).count()

    subject_scores = {}
    for score in user_scores:
        quiz = Quiz.query.get(score.quiz_id)
        subject = Subject.query.get(quiz.subject_id)
        subject_name = subject.name

        if subject_name not in subject_scores:
            subject_scores[subject_name] = []
        subject_scores[subject_name].append(score.marks)

    subject_avg_scores = {}
    best_subject = None
    weakest_subject = None
    overall_avg_score = 0

    if subject_scores:
        subject_avg_scores = {
            subject: round(sum(scores) / len(scores), 2)
            for subject, scores in subject_scores.items()
        }
        best_subject = max(subject_avg_scores, key=subject_avg_scores.get)
        weakest_subject = min(subject_avg_scores, key=subject_avg_scores.get)

        all_marks = [mark for scores in subject_scores.values() for mark in scores]
        overall_avg_score = round(sum(all_marks) / len(all_marks), 2)

    return render_template(
        "user_stats.html",
        user=user,
        total_chapters_saved=total_chapters_saved,
        total_quizzes_attempted=total_quizzes_attempted,
        overall_avg_score=overall_avg_score,
        subject_avg_scores=subject_avg_scores,
        best_subject=best_subject,
        weakest_subject=weakest_subject,
    )

@stats.route("/adminhome/analytics")
def admin_analytics():
    users = User.query.all()
    educators = Educator.query.all()
    total_users = len(users)
    user_avg_scores = {}
    educator_scores = {}  
    for user in users:
        user_scores = (
            Score.query.filter_by(user_id=user.id)
            .order_by(Score.id.desc())
            .all()
        )
        latest_scores = {}
        for score in user_scores:
            if score.quiz_id not in latest_scores:
                latest_scores[score.quiz_id] = score
        if latest_scores:
            avg_score = round(
                sum(score.marks for score in latest_scores.values()) / len(latest_scores),
                2,
            )
            user_avg_scores[user.username] = avg_score
    best_user = max(user_avg_scores, key=user_avg_scores.get) if user_avg_scores else None
    worst_user = min(user_avg_scores, key=user_avg_scores.get) if user_avg_scores else None
    subject_enrollments = {}
    for enrollment in Enrollment.query.all():
        subject_name = Subject.query.get(enrollment.subject_id).name
        subject_enrollments[subject_name] = subject_enrollments.get(subject_name, 0) + 1
    most_popular_subject = max(subject_enrollments, key=subject_enrollments.get) if subject_enrollments else None
    for educator in educators:
        educator_scores_list = []
        for subject in educator.subject:
            enrolled_users = User.query.join(Enrollment).filter(Enrollment.subject_id == subject.id).all()
            for user in enrolled_users:
                scores = Score.query.filter_by(user_id=user.id).all()
                for score in scores:
                    educator_scores_list.append(score.marks)
        if educator_scores_list:
            avg_score = round(sum(educator_scores_list) / len(educator_scores_list), 2)
            educator_scores[educator.fullname] = avg_score
    best_educator = max(educator_scores, key=educator_scores.get) if educator_scores else None
    worst_educator = min(educator_scores, key=educator_scores.get) if educator_scores else None
    return render_template(
        "admin_analytics.html",
        total_users=total_users,
        best_user=best_user,
        worst_user=worst_user,
        most_popular_subject=most_popular_subject,
        user_avg_scores=user_avg_scores,
        best_educator=best_educator,
        worst_educator=worst_educator,
        educator_scores=educator_scores, 
    )

@stats.route("/educatorhome/analytics/<int:educator_id>", methods=["GET"])
def educator_analytics(educator_id):
    educator = Educator.query.get(educator_id)
    if not educator:
        flash("Educator not found!", category="error")
        return redirect("/")
    subjects = Subject.query.filter_by(educator_id=educator_id).all()
    subject_ids = [subject.id for subject in subjects]
    enrollments = Enrollment.query.filter(Enrollment.subject_id.in_(subject_ids)).all()
    user_scores = {}
    for enrollment in enrollments:
        user_id = enrollment.user_id
        if user_id not in user_scores:
            user = User.query.get(user_id)
            user_scores[user_id] = {
                "user": user,
                "total_score": 0,
                "subject_count": 0
            }
        user_scores[user_id]["total_score"] += enrollment.score 
        user_scores[user_id]["subject_count"] += 1
    leaderboard = sorted(user_scores.values(), key=lambda x: x["total_score"], reverse=True)
    subject_popularity = {}
    for subject in subjects:
        count = Enrollment.query.filter_by(subject_id=subject.id).count()
        subject_popularity[subject] = count
    popular_subjects = sorted(subject_popularity.items(), key=lambda x: x[1], reverse=True)
    return render_template("educator_analytics.html",
                           educator=educator,
                           leaderboard=leaderboard,
                           popular_subjects=popular_subjects)

@stats.route("/userhome/<int:user_id>/stats")

def view_stats_user(user_id):
    user = User.query.get(user_id)

    user_scores = (
        Score.query.filter_by(user_id=user_id)
        .order_by(Score.id.desc()) 
        .all()
    )

    latest_scores = {}
    for score in user_scores:
        if score.quiz_id not in latest_scores:
            latest_scores[score.quiz_id] = score

    quiz_data = []
    subject_scores = {}

    subject_avg_scores = {}
    best_subject = None
    weakest_subject = None

    for quiz_id, score in latest_scores.items():
        quiz = Quiz.query.get(quiz_id)
        
        subject = Subject.query.get(quiz.subject_id)

        quiz_data.append({
            "subject_name": subject.name,
            "quiz_name": quiz.name,
            "latest_score": score.marks
        })

        if subject.name not in subject_scores:
            subject_scores[subject.name] = []
        subject_scores[subject.name].append(score.marks)

    if subject_scores:
        subject_avg_scores = {subject: round(sum(scores) / len(scores), 2) for subject, scores in subject_scores.items()}
        best_subject = max(subject_avg_scores, key=subject_avg_scores.get)
        weakest_subject = min(subject_avg_scores, key=subject_avg_scores.get)

    return render_template(
        "personal_user_stats.html", 
        user=user, 
        quiz_data=quiz_data, 
        quiz_count=len(quiz_data), 
        subject_avg_scores=subject_avg_scores, 
        best_subject=best_subject, 
        weakest_subject=weakest_subject
    )