"""
app.py
Main Flask application: routing, auth, quiz API, and admin panel
for the Quiz Application.
"""

import os
import functools
from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, flash
)

import models
from database import init_app_db, CATEGORIES

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

QUESTIONS_PER_QUIZ = 10
SECONDS_PER_QUESTION = 45  # used to compute total quiz time on the client


# ---------------------------------------------------------------------
# Decorators / helpers
# ---------------------------------------------------------------------

def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session or not session.get("is_admin"):
            flash("Admin access required.", "error")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped


def current_user():
    if "user_id" in session:
        return models.get_user_by_id(session["user_id"])
    return None


@app.context_processor
def inject_user():
    return {"logged_in_user": current_user(), "categories_list": CATEGORIES}


# ---------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("All fields are required.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        elif password != confirm:
            flash("Passwords do not match.", "error")
        else:
            ok, message = models.create_user(username, email, password)
            flash(message, "success" if ok else "error")
            if ok:
                return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = models.verify_login(username, password)
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = bool(user["is_admin"])
            flash(f"Welcome back, {user['username']}!", "success")
            if user["is_admin"]:
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html", is_admin=False)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


# ---------------------------------------------------------------------
# User area
# ---------------------------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    categories = models.get_categories_with_counts()
    stats = models.get_user_stats(session["user_id"])
    return render_template("dashboard.html", categories=categories, stats=stats)


@app.route("/quiz/<category>")
@login_required
def quiz(category):
    if category not in CATEGORIES:
        flash("Unknown category.", "error")
        return redirect(url_for("dashboard"))
    total_seconds = QUESTIONS_PER_QUIZ * SECONDS_PER_QUESTION
    return render_template(
        "quiz.html", category=category, total_seconds=total_seconds
    )


@app.route("/api/quiz/questions/<category>")
@login_required
def api_quiz_questions(category):
    if category not in CATEGORIES:
        return jsonify({"error": "Unknown category"}), 400
    rows = models.get_random_questions(category, QUESTIONS_PER_QUIZ)
    questions = [
        {
            "id": row["id"],
            "question_text": row["question_text"],
            "options": {
                "A": row["option_a"],
                "B": row["option_b"],
                "C": row["option_c"],
                "D": row["option_d"],
            },
            "difficulty": row["difficulty"],
        }
        for row in rows
    ]
    return jsonify({
        "category": category,
        "total_seconds": QUESTIONS_PER_QUIZ * SECONDS_PER_QUESTION,
        "questions": questions,
    })


@app.route("/api/quiz/submit", methods=["POST"])
@login_required
def api_quiz_submit():
    data = request.get_json(force=True, silent=True) or {}
    category = data.get("category")
    answers = data.get("answers", {})  # {question_id(str): "A"/"B"/"C"/"D"}
    time_taken = int(data.get("time_taken", 0))

    if category not in CATEGORIES or not isinstance(answers, dict):
        return jsonify({"error": "Invalid submission"}), 400

    question_ids = [int(qid) for qid in answers.keys()]
    question_map = models.get_questions_by_ids(question_ids)

    score = 0
    details = []
    for qid_str, selected in answers.items():
        qid = int(qid_str)
        question = question_map.get(qid)
        if not question:
            continue
        is_correct = (selected == question["correct_option"])
        if is_correct:
            score += 1
        details.append({
            "id": qid,
            "question_text": question["question_text"],
            "your_answer": selected,
            "correct_answer": question["correct_option"],
            "is_correct": is_correct,
        })

    total_questions = len(question_map)
    result_id = models.save_result(
        session["user_id"], category, score, total_questions, time_taken
    )

    return jsonify({
        "result_id": result_id,
        "score": score,
        "total_questions": total_questions,
    })


@app.route("/result/<int:result_id>")
@login_required
def result(result_id):
    row = models.get_result_by_id(result_id)
    if not row or row["user_id"] != session["user_id"]:
        flash("Result not found.", "error")
        return redirect(url_for("dashboard"))
    percent = round((row["score"] / row["total_questions"]) * 100, 1) if row["total_questions"] else 0
    return render_template("result.html", result=row, percent=percent)


@app.route("/leaderboard")
@login_required
def leaderboard():
    category = request.args.get("category")
    if category and category not in CATEGORIES:
        category = None
    rows = models.get_leaderboard(category)
    return render_template("leaderboard.html", rows=rows, selected_category=category)


@app.route("/profile")
@login_required
def profile():
    user = current_user()
    results = models.get_user_results(session["user_id"])
    stats = models.get_user_stats(session["user_id"])
    return render_template("profile.html", user=user, results=results, stats=stats)


# ---------------------------------------------------------------------
# Admin area
# ---------------------------------------------------------------------

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = models.verify_login(username, password)
        if user and user["is_admin"]:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = True
            flash("Welcome back, admin.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Invalid admin credentials.", "error")
    return render_template("login.html", is_admin=True)


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    questions = models.get_all_questions()
    users = models.get_all_users()
    return render_template(
        "admin.html", questions=questions, users=users, categories=CATEGORIES
    )


@app.route("/admin/questions/add", methods=["POST"])
@admin_required
def admin_add_question():
    category = request.form.get("category")
    question_text = request.form.get("question_text", "").strip()
    option_a = request.form.get("option_a", "").strip()
    option_b = request.form.get("option_b", "").strip()
    option_c = request.form.get("option_c", "").strip()
    option_d = request.form.get("option_d", "").strip()
    correct_option = request.form.get("correct_option")
    difficulty = request.form.get("difficulty", "Medium")

    if (category not in CATEGORIES or not question_text or not option_a or
            not option_b or not option_c or not option_d or
            correct_option not in ("A", "B", "C", "D")):
        flash("Please fill in all fields correctly.", "error")
    else:
        models.add_question(category, question_text, option_a, option_b,
                             option_c, option_d, correct_option, difficulty)
        flash("Question added successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/questions/delete/<int:question_id>", methods=["POST"])
@admin_required
def admin_delete_question(question_id):
    models.delete_question(question_id)
    flash("Question deleted.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
@admin_required
def admin_delete_user(user_id):
    models.delete_user(user_id)
    flash("User deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

init_app_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
