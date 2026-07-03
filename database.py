"""
database.py
Handles the raw SQLite connection, schema creation, and seed data
for the Quiz Application.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quiz.db")

CATEGORIES = ["HTML", "CSS", "JavaScript", "Python", "DBMS", "DSA"]


def get_db_connection():
    """Return a new SQLite connection with rows accessible by column name."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not already exist."""
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question_text TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL CHECK (correct_option IN ('A','B','C','D')),
            difficulty TEXT NOT NULL DEFAULT 'Medium',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            time_taken INTEGER NOT NULL DEFAULT 0,
            date_taken TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def seed_admin():
    """Create a default admin account if one does not exist."""
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT id FROM users WHERE is_admin = 1"
    ).fetchone()
    if not existing:
        conn.execute(
            "INSERT INTO users (username, email, password_hash, is_admin) "
            "VALUES (?, ?, ?, 1)",
            ("admin", "admin@quizapp.com", generate_password_hash("admin123")),
        )
        conn.commit()
    conn.close()


def seed_questions():
    """Populate sample questions for every category if the table is empty."""
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) AS c FROM questions").fetchone()["c"]
    if count > 0:
        conn.close()
        return

    sample_questions = [
        # HTML
        ("HTML", "What does HTML stand for?", "Hyper Trainer Marking Language",
         "Hyper Text Markup Language", "Hyper Text Marketing Language",
         "Hyper Tool Multi Language", "B", "Easy"),
        ("HTML", "Which tag is used to create a hyperlink?", "<link>", "<a>",
         "<href>", "<hyper>", "B", "Easy"),
        ("HTML", "Which attribute specifies an alternate text for an image?",
         "src", "alt", "title", "longdesc", "B", "Easy"),
        ("HTML", "Which HTML element defines the title of a document?",
         "<meta>", "<head>", "<title>", "<header>", "C", "Easy"),
        ("HTML", "Which tag is used to define an internal style sheet?",
         "<css>", "<script>", "<style>", "<link>", "C", "Medium"),
        ("HTML", "What is the correct HTML for making a checkbox?",
         "<input type='check'>", "<checkbox>", "<input type='checkbox'>",
         "<check>", "C", "Medium"),
        ("HTML", "Which element is used to specify a footer for a document?",
         "<bottom>", "<footer>", "<section>", "<foot>", "B", "Easy"),
        ("HTML", "Which doctype is correct for HTML5?", "<!DOCTYPE html5>",
         "<!DOCTYPE HTML PUBLIC>", "<!DOCTYPE html>", "<!DTD html>", "C", "Easy"),

        # CSS
        ("CSS", "What does CSS stand for?", "Creative Style Sheets",
         "Cascading Style Sheets", "Computer Style Sheets",
         "Colorful Style Sheets", "B", "Easy"),
        ("CSS", "Which property is used to change the background color?",
         "color", "bgcolor", "background-color", "background", "C", "Easy"),
        ("CSS", "How do you select an element with id 'demo'?", ".demo",
         "*demo", "#demo", "demo", "C", "Easy"),
        ("CSS", "Which property controls the text size?", "font-style",
         "text-size", "font-size", "text-style", "C", "Easy"),
        ("CSS", "Which CSS property is used for the spacing between the border and content?",
         "margin", "padding", "spacing", "border-spacing", "B", "Medium"),
        ("CSS", "Which value of position property positions relative to viewport?",
         "relative", "absolute", "fixed", "static", "C", "Medium"),
        ("CSS", "Which of these is a valid CSS flexbox property?",
         "flex-direction", "flex-flow-x", "box-flex", "flex-align", "A", "Medium"),
        ("CSS", "What does 'em' unit represent in CSS?",
         "Fixed pixel value", "Relative to root font size",
         "Relative to parent font size", "Percentage of viewport", "C", "Hard"),

        # JavaScript
        ("JavaScript", "Which company developed JavaScript?", "Microsoft",
         "Netscape", "Sun Microsystems", "Google", "B", "Easy"),
        ("JavaScript", "How do you declare a variable in modern JS?", "var x;",
         "let x;", "int x;", "variable x;", "B", "Easy"),
        ("JavaScript", "Which method converts JSON to a JS object?",
         "JSON.parse()", "JSON.stringify()", "JSON.toObject()",
         "JSON.convert()", "A", "Medium"),
        ("JavaScript", "What does '===' check in JavaScript?",
         "Value only", "Type only", "Value and type", "Reference only",
         "C", "Medium"),
        ("JavaScript", "Which function is used to parse a string to an integer?",
         "Integer.parse()", "parseInt()", "toInt()", "Number.int()", "B", "Easy"),
        ("JavaScript", "What is the correct way to write an arrow function?",
         "function => {}", "() => {}", "=> () {}", "function() -> {}",
         "B", "Medium"),
        ("JavaScript", "Which keyword is used to handle exceptions?",
         "catch", "throws", "handle", "except", "A", "Medium"),
        ("JavaScript", "What is the output type of typeof null?",
         "'null'", "'undefined'", "'object'", "'boolean'", "C", "Hard"),

        # Python
        ("Python", "Which keyword is used to define a function in Python?",
         "func", "def", "function", "define", "B", "Easy"),
        ("Python", "What is the output of type([])?", "<class 'list'>",
         "<class 'array'>", "<class 'tuple'>", "<class 'dict'>", "A", "Easy"),
        ("Python", "Which of these is used for comments in Python?", "//",
         "/* */", "#", "--", "C", "Easy"),
        ("Python", "What does 'len()' do?", "Returns the type",
         "Returns the length", "Returns the last element",
         "Returns memory location", "B", "Easy"),
        ("Python", "Which data type is immutable in Python?", "list", "dict",
         "set", "tuple", "D", "Medium"),
        ("Python", "What is the correct file extension for Python files?",
         ".py", ".python", ".pt", ".pyt", "A", "Easy"),
        ("Python", "Which module is used for regular expressions?", "regex",
         "re", "pyregex", "regexp", "B", "Medium"),
        ("Python", "What does the 'self' keyword represent in a class?",
         "The class itself", "The current instance", "A static variable",
         "The parent class", "B", "Medium"),

        # DBMS
        ("DBMS", "What does DBMS stand for?", "Database Management System",
         "Data Backup Management System", "Database Modeling System",
         "Data Management Software", "A", "Easy"),
        ("DBMS", "Which SQL command is used to remove a table?", "DELETE",
         "REMOVE", "DROP", "TRUNCATE", "C", "Easy"),
        ("DBMS", "Which normal form removes transitive dependency?", "1NF",
         "2NF", "3NF", "BCNF", "C", "Medium"),
        ("DBMS", "Which key uniquely identifies a record in a table?",
         "Foreign key", "Primary key", "Candidate key", "Composite key",
         "B", "Easy"),
        ("DBMS", "Which SQL clause is used to filter groups?", "WHERE",
         "HAVING", "GROUP BY", "FILTER", "B", "Medium"),
        ("DBMS", "What type of join returns only matching rows?", "LEFT JOIN",
         "RIGHT JOIN", "INNER JOIN", "FULL JOIN", "C", "Medium"),
        ("DBMS", "Which property ensures database transactions are reliable?",
         "ACID", "BASE", "CRUD", "SOLID", "A", "Hard"),
        ("DBMS", "Which command is used to give user access privileges?",
         "GRANT", "ALLOW", "PERMIT", "ACCESS", "A", "Medium"),

        # DSA
        ("DSA", "What is the time complexity of binary search?", "O(n)",
         "O(log n)", "O(n log n)", "O(1)", "B", "Easy"),
        ("DSA", "Which data structure uses FIFO order?", "Stack", "Queue",
         "Tree", "Graph", "B", "Easy"),
        ("DSA", "Which sorting algorithm has the best average case of O(n log n)?",
         "Bubble Sort", "Insertion Sort", "Merge Sort", "Selection Sort",
         "C", "Medium"),
        ("DSA", "What is the worst-case time complexity of quicksort?",
         "O(n log n)", "O(n)", "O(n^2)", "O(log n)", "C", "Hard"),
        ("DSA", "Which data structure is used for recursion internally?",
         "Queue", "Stack", "Heap", "Array", "B", "Easy"),
        ("DSA", "What does a hash table use to store key-value pairs?",
         "Linked list only", "Hash function", "Binary tree", "Stack",
         "B", "Medium"),
        ("DSA", "Which traversal visits the root node first?", "Inorder",
         "Preorder", "Postorder", "Level order", "B", "Medium"),
        ("DSA", "What is the space complexity of merge sort?", "O(1)",
         "O(log n)", "O(n)", "O(n^2)", "C", "Hard"),
    ]

    conn.executemany(
        "INSERT INTO questions "
        "(category, question_text, option_a, option_b, option_c, option_d, "
        "correct_option, difficulty) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        sample_questions,
    )
    conn.commit()
    conn.close()


def init_app_db():
    """Convenience entry point: create schema and seed initial data."""
    init_db()
    seed_admin()
    seed_questions()
