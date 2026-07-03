<div align="center">

# 🎯 QuizMaster
### 🚀 Professional Full-Stack Quiz Application

<p align="center">
A modern <b>Flask + SQLite</b> powered quiz platform inspired by online assessment systems used by colleges and companies.
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white">
<img src="https://img.shields.io/badge/Flask-2.x-black?style=for-the-badge&logo=flask">
<img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite">
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
</p>

<p align="center">
<img src="https://img.shields.io/github/license/yourusername/QuizMaster?style=flat-square">
<img src="https://img.shields.io/github/stars/yourusername/QuizMaster?style=flat-square">
<img src="https://img.shields.io/github/forks/yourusername/QuizMaster?style=flat-square">
<img src="https://img.shields.io/github/issues/yourusername/QuizMaster?style=flat-square">
</p>

---

### 🌟 Build • Practice • Learn • Compete

</div>

---

# 📖 About

**QuizMaster** is a professional web-based quiz platform developed using **Flask**, **SQLite**, and **Vanilla JavaScript**.

The application provides an interactive quiz environment featuring secure authentication, timer-based quizzes, leaderboards, admin management, progress tracking, and responsive design.

Perfect for:

- 🎓 Colleges
- 🏫 Schools
- 💼 Company Assessments
- 📚 Self Learning
- 💻 Portfolio Projects

---

# ✨ Features

## 👨‍🎓 User Features

- 🔐 Secure User Registration & Login
- 🔒 Password Hashing using Werkzeug
- 📊 Personal Dashboard
- 📚 Six Quiz Categories
- 🎲 Random Question Generator
- ⏱ Countdown Timer
- 📈 Progress Bar
- ⏭ Next & Previous Navigation
- 🔢 Question Jump Panel
- 📝 Automatic Submission
- 🎯 Instant Score Calculation
- 📜 Quiz History
- 🏆 Leaderboard
- 👤 User Profile
- 📱 Fully Responsive UI

---

## 👨‍💼 Admin Features

- 🔑 Separate Admin Login
- ➕ Add Questions
- ❌ Delete Questions
- 👥 View Users
- 🚫 Delete Users
- 📊 Manage Quiz Database

---

# 📚 Available Quiz Categories

| Category | Questions |
|-----------|-----------|
| 🌐 HTML | 8+ |
| 🎨 CSS | 8+ |
| ⚡ JavaScript | 8+ |
| 🐍 Python | 8+ |
| 🗄 DBMS | 8+ |
| 💡 DSA | 8+ |

> Total Sample Questions: **48+**

---

# 🏗 Project Structure

```text
Quiz-App/
│
├── app.py                     # Flask Application
├── database.py                # SQLite Schema + Seed Data
├── models.py                  # Database Queries
├── requirements.txt
│
├── static/
│   ├── css/
│   │      style.css
│   │
│   └── js/
│       ├── script.js
│       ├── timer.js
│       ├── quiz.js
│       └── admin.js
│
├── templates/
│     ├── login.html
│     ├── register.html
│     ├── dashboard.html
│     ├── quiz.html
│     ├── result.html
│     └── ...
│
└── quiz.db
```

---

# ⚙ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/QuizMaster.git

cd QuizMaster
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Application

```bash
python app.py
```

---

## 4️⃣ Open Browser

```
http://localhost:5000
```

---

# 🛠 Default Admin Credentials

| Field | Value |
|-------|-------|
| Username | admin |
| Password | admin123 |

> ⚠ Change the default admin password before deploying publicly.

---

# 🔄 Quiz Workflow

```text
User Login
      │
      ▼
Choose Category
      │
      ▼
Fetch Random Questions
      │
      ▼
Start Countdown Timer
      │
      ▼
Answer Questions
      │
      ▼
Manual / Auto Submit
      │
      ▼
Server-side Evaluation
      │
      ▼
Result Stored
      │
      ▼
Score Display
```

---

# 🗃 Database

Automatically created on first run.

Includes:

- Users
- Questions
- Results
- Categories
- Admin Account

---

# 🚀 Deployment

## Render

```bash
Build Command

pip install -r requirements.txt
```

```bash
Start Command

gunicorn app:app
```

Environment Variable

```text
SECRET_KEY=your_secret_key
```

---

## Railway

Deploy directly from GitHub.

Start Command

```bash
gunicorn app:app
```

Environment Variable

```text
SECRET_KEY=your_secret_key
```

---

# ⚠ SQLite Note

Free hosting providers use **ephemeral storage**.

This means:

- Database resets after restart
- Data is temporary

For production:

- PostgreSQL
- MySQL
- Render Persistent Disk

---

# 🔐 Security Recommendations

✅ Change Admin Password

✅ Set SECRET_KEY

✅ Use HTTPS

✅ Enable Rate Limiting

✅ Validate Inputs

✅ Use Environment Variables

---

# 💻 Tech Stack

| Layer | Technology |
|---------|-----------|
| Frontend | HTML5 |
| Styling | CSS3 |
| Programming | JavaScript |
| Backend | Flask |
| Language | Python |
| Database | SQLite |
| Authentication | Flask Sessions |
| Password Security | Werkzeug |
| Deployment | Render / Railway |
| Server | Gunicorn |

---

# 📸 Screenshots

```
📷 Add screenshots here

Home Page
Dashboard
Quiz Page
Leaderboard
Admin Panel
Results
```

---

# 🌱 Future Improvements

- 🎨 Dark Mode
- 📧 Email Verification
- 📄 PDF Certificates
- 🏅 Achievements & Badges
- 📊 Analytics Dashboard
- 📱 Progressive Web App
- 🔔 Notifications
- 🌍 Multi-language Support

---

# 🤝 Contributing

Contributions are always welcome!

```bash
Fork the Repository

Create a Feature Branch

Commit Changes

Push Changes

Create Pull Request
```

---

# ⭐ Support

If you like this project,

⭐ Star the Repository

🍴 Fork the Repository

🐞 Report Issues

💡 Suggest New Features

---

# 👨‍💻 Developer

## **Saksham Jha**

**Computer Science Student | Full Stack Developer | Python Developer**

### Connect with Me

<p align="left">

<a href="https://github.com/yourusername">
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github">
</a>

<a href="https://linkedin.com/in/yourprofile">
<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin">
</a>

<a href="mailto:your@email.com">
<img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail">
</a>

</p>

---

<div align="center">

## ⭐ If you found this project useful, don't forget to Star the Repository ⭐

Made with ❤️ by **Saksham Jha**

</div>
