"""
models.py
Data-access layer. Every function opens its own short-lived SQLite
connection (safe for Flask's threaded dev server and simple WSGI workers).
"""

import random
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db_connection, CATEGORIES


# ---------------------------------------------------------------------
# USERS
# ---------------------------------------------------------------------

def create_user(username, email, password):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, generate_password_hash(password)),
        )
        conn.commit()
        return True, "Account created successfully."
    except Exception as exc:
        if "UNIQUE" in str(exc):
            return False, "Username or email already exists."
        return False, "Could not create account."
    finally:
        conn.close()


def get_user_by_username(username):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return user


def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return user


def verify_login(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_all_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT id, username, email, is_admin, created_at FROM users "
        "ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return users


def delete_user(user_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ? AND is_admin = 0", (user_id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------
# QUESTIONS
# ---------------------------------------------------------------------

def get_categories_with_counts():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT category, COUNT(*) AS total FROM questions GROUP BY category"
    ).fetchall()
    conn.close()
    counts = {row["category"]: row["total"] for row in rows}
    return [{"name": c, "count": counts.get(c, 0)} for c in CATEGORIES]


def get_random_questions(category, limit=10):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, category, question_text, option_a, option_b, "
        "option_c, option_d, difficulty FROM questions WHERE category = ?",
        (category,),
    ).fetchall()
    conn.close()
    rows = list(rows)
    random.shuffle(rows)
    return rows[:limit]


def get_questions_by_ids(question_ids):
    if not question_ids:
        return []
    conn = get_db_connection()
    placeholders = ",".join("?" for _ in question_ids)
    rows = conn.execute(
        f"SELECT * FROM questions WHERE id IN ({placeholders})", question_ids
    ).fetchall()
    conn.close()
    return {row["id"]: row for row in rows}


def get_all_questions(category=None):
    conn = get_db_connection()
    if category:
        rows = conn.execute(
            "SELECT * FROM questions WHERE category = ? ORDER BY id DESC",
            (category,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM questions ORDER BY id DESC"
        ).fetchall()
    conn.close()
    return rows


def add_question(category, question_text, option_a, option_b, option_c,
                  option_d, correct_option, difficulty="Medium"):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO questions (category, question_text, option_a, option_b, "
        "option_c, option_d, correct_option, difficulty) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (category, question_text, option_a, option_b, option_c, option_d,
         correct_option, difficulty),
    )
    conn.commit()
    conn.close()


def delete_question(question_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------
# RESULTS / LEADERBOARD
# ---------------------------------------------------------------------

def save_result(user_id, category, score, total_questions, time_taken):
    conn = get_db_connection()
    cur = conn.execute(
        "INSERT INTO results (user_id, category, score, total_questions, "
        "time_taken) VALUES (?, ?, ?, ?, ?)",
        (user_id, category, score, total_questions, time_taken),
    )
    conn.commit()
    result_id = cur.lastrowid
    conn.close()
    return result_id


def get_result_by_id(result_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT results.*, users.username FROM results "
        "JOIN users ON users.id = results.user_id WHERE results.id = ?",
        (result_id,),
    ).fetchone()
    conn.close()
    return row


def get_user_results(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM results WHERE user_id = ? ORDER BY date_taken DESC",
        (user_id,),
    ).fetchall()
    conn.close()
    return rows


def get_user_stats(user_id):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT COUNT(*) AS attempts, "
        "COALESCE(AVG(score * 100.0 / total_questions), 0) AS avg_percent, "
        "COALESCE(MAX(score * 100.0 / total_questions), 0) AS best_percent "
        "FROM results WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    return row


def get_leaderboard(category=None, limit=20):
    conn = get_db_connection()
    if category:
        rows = conn.execute(
            "SELECT users.username, results.category, "
            "MAX(results.score * 100.0 / results.total_questions) AS best_percent, "
            "MAX(results.score) AS best_score, results.total_questions, "
            "MIN(results.time_taken) AS best_time "
            "FROM results JOIN users ON users.id = results.user_id "
            "WHERE results.category = ? "
            "GROUP BY users.id "
            "ORDER BY best_percent DESC, best_time ASC LIMIT ?",
            (category, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT users.username, "
            "COUNT(results.id) AS attempts, "
            "COALESCE(AVG(results.score * 100.0 / results.total_questions), 0) "
            "AS best_percent "
            "FROM results JOIN users ON users.id = results.user_id "
            "GROUP BY users.id "
            "ORDER BY best_percent DESC LIMIT ?",
            (limit,),
        ).fetchall()
    conn.close()
    return rows
