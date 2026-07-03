# QuizMaster — Professional Quiz Application

A full-stack quiz platform built with **Flask + SQLite + vanilla JS**, in the
style of assessment tools used by companies and colleges.

## Features

- User registration & login (hashed passwords via Werkzeug)
- Dashboard with per-category question counts and personal stats
- 6 categories out of the box: HTML, CSS, JavaScript, Python, DBMS, DSA
- Randomized 10-question quizzes pulled from a growing question bank
- Countdown timer with auto-submit when time runs out
- Next / Previous navigation with a question-jump map and progress bar
- Score calculation, results page, and quiz history
- Leaderboard (overall and per-category)
- User profile with quiz history and stats
- Separate admin login, with:
  - Add questions
  - Delete questions
  - View & delete users
- Fully responsive design (mobile nav, fluid grids)

## Project Structure

```
Quiz-App/
├── app.py                 # Flask routes & app entry point
├── database.py             # SQLite schema + seed data
├── models.py                # Data-access layer (queries)
├── requirements.txt
├── static/
│   ├── css/style.css        # Design system (scantron/exam-sheet theme)
│   ├── js/script.js          # Nav + flash messages
│   ├── js/timer.js            # Reusable countdown timer
│   ├── js/quiz.js              # Quiz-taking logic (fetch, nav, submit)
│   └── js/admin.js              # Admin tab switching
├── templates/                    # Jinja2 templates (one per page)
└── quiz.db                        # Created automatically on first run
```

## Local Setup

1. **Install dependencies** (Python 3.9+ recommended):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**:
   ```bash
   python app.py
   ```
   The database (`quiz.db`) and all tables are created automatically on
   first run, along with 48 sample questions (8 per category) and a
   default admin account.

3. **Open** `http://localhost:5000` in your browser.

### Default Admin Login
- URL: `/admin/login`
- Username: `admin`
- Password: `admin123`

**Change this password (or delete/recreate the admin user) before deploying
publicly** — see "Security notes" below.

## How the Quiz Flow Works

1. A logged-in user picks a category on `/dashboard`.
2. `/quiz/<category>` loads a page shell; JavaScript fetches 10 random
   questions from `/api/quiz/questions/<category>` (correct answers are
   never sent to the client).
3. The user answers, navigates with Next/Previous or the jump-dots, and a
   countdown timer runs the whole time.
4. On submit (manual or automatic via timer expiry), all answers are POSTed
   to `/api/quiz/submit`, which grades them server-side, stores a `Result`
   row, and returns a `result_id`.
5. The browser redirects to `/result/<id>` to show the score.

## Deployment (Render or Railway)

Both platforms can run this app directly from the repo.

### Render
1. Push this project to a GitHub repository.
2. In Render, create a **New Web Service** from that repo.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Add an environment variable `SECRET_KEY` with a random secret string.

### Railway
1. Push to GitHub, then **New Project → Deploy from GitHub repo**.
2. Railway auto-detects Python; set the start command to `gunicorn app:app`
   if it isn't picked up automatically.
3. Add a `SECRET_KEY` environment variable in the Railway dashboard.

### Important: SQLite on these platforms
Render's and Railway's filesystems are **ephemeral on the free tier** —
`quiz.db` will reset on every redeploy/restart. For a persistent database:
- Render: attach a **persistent disk** and point `quiz.db` at it (or switch
  to their managed Postgres and swap `sqlite3` calls for `psycopg2`).
- Railway: add their **Postgres plugin** for production use.

For a class project, demo, or portfolio piece, the default SQLite file is
fine as-is.

## Security Notes Before Going Public

- Set a strong, random `SECRET_KEY` via environment variable (already wired
  up in `app.py` via `os.environ.get("SECRET_KEY", ...)`).
- Change the default admin password immediately, or delete the seeded
  admin row and create your own via the database.
- Consider adding rate-limiting to `/login` and `/register` if this will be
  publicly exposed.

## Tech Stack

| Layer      | Technology                        |
|------------|------------------------------------|
| Frontend   | HTML5, CSS3 (custom design system), vanilla JS |
| Backend    | Flask (Python)                    |
| Database   | SQLite (via Python's `sqlite3`)   |
| Auth       | Flask sessions + Werkzeug password hashing |
| Deployment | Render / Railway (gunicorn)       |
