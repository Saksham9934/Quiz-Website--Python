/* quiz.js — drives the quiz-taking experience on quiz.html */

document.addEventListener("DOMContentLoaded", () => {
    const wrapper = document.getElementById("quizWrapper");
    if (!wrapper) return;

    const category = wrapper.dataset.category;
    const totalSecondsFallback = parseInt(wrapper.dataset.totalSeconds, 10) || 450;

    const loadingState = document.getElementById("loadingState");
    const quizBody = document.getElementById("quizBody");
    const questionCounter = document.getElementById("questionCounter");
    const timerDisplay = document.getElementById("timerDisplay");
    const timerBox = document.querySelector(".timer-box");
    const progressFill = document.getElementById("progressFill");
    const questionText = document.getElementById("questionText");
    const optionsList = document.getElementById("optionsList");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const submitBtn = document.getElementById("submitBtn");
    const questionJump = document.getElementById("questionJump");

    const confirmModal = document.getElementById("confirmModal");
    const answeredCountEl = document.getElementById("answeredCount");
    const totalCountEl = document.getElementById("totalCount");
    const cancelSubmit = document.getElementById("cancelSubmit");
    const confirmSubmit = document.getElementById("confirmSubmit");

    let questions = [];
    let answers = {};        // { questionId(string): "A"/"B"/"C"/"D" }
    let currentIndex = 0;
    let timer = null;
    let submitted = false;

    fetch(`/api/quiz/questions/${encodeURIComponent(category)}`)
        .then((res) => {
            if (!res.ok) throw new Error("Failed to load questions");
            return res.json();
        })
        .then((data) => {
            questions = data.questions;
            const totalSeconds = data.total_seconds || totalSecondsFallback;

            if (!questions.length) {
                loadingState.innerHTML = "<p>No questions available for this category yet.</p>";
                return;
            }

            buildJumpDots();
            renderQuestion(0);

            loadingState.style.display = "none";
            quizBody.style.display = "block";

            timer = createTimer(totalSeconds, {
                onTick: (secondsLeft, formatted) => {
                    timerDisplay.textContent = formatted;
                    if (secondsLeft <= 30) {
                        timerBox.classList.add("timer-warning");
                    }
                },
                onExpire: () => {
                    submitQuiz(true);
                },
            });
            timer.start();
        })
        .catch(() => {
            loadingState.innerHTML = "<p>Could not load the quiz. Please go back and try again.</p>";
        });

    function buildJumpDots() {
        questionJump.innerHTML = "";
        questions.forEach((q, idx) => {
            const dot = document.createElement("div");
            dot.className = "jump-dot";
            dot.textContent = idx + 1;
            dot.addEventListener("click", () => renderQuestion(idx));
            questionJump.appendChild(dot);
        });
    }

    function updateJumpDots() {
        const dots = questionJump.querySelectorAll(".jump-dot");
        dots.forEach((dot, idx) => {
            dot.classList.toggle("current", idx === currentIndex);
            dot.classList.toggle("answered", !!answers[questions[idx].id]);
        });
    }

    function renderQuestion(index) {
        currentIndex = index;
        const q = questions[index];

        questionCounter.textContent = `Question ${index + 1} of ${questions.length}`;
        questionText.textContent = q.question_text;
        progressFill.style.width = `${((index + 1) / questions.length) * 100}%`;

        optionsList.innerHTML = "";
        Object.entries(q.options).forEach(([letter, text]) => {
            const item = document.createElement("div");
            item.className = "option-item";
            if (answers[q.id] === letter) item.classList.add("selected");

            item.innerHTML = `
                <div class="option-bubble">${letter}</div>
                <div class="option-text">${escapeHtml(text)}</div>
            `;
            item.addEventListener("click", () => selectAnswer(q.id, letter));
            optionsList.appendChild(item);
        });

        prevBtn.disabled = index === 0;
        nextBtn.textContent = index === questions.length - 1 ? "Finish" : "Next →";

        updateJumpDots();
    }

    function selectAnswer(questionId, letter) {
        answers[questionId] = letter;
        renderQuestion(currentIndex);
    }

    function escapeHtml(str) {
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    prevBtn.addEventListener("click", () => {
        if (currentIndex > 0) renderQuestion(currentIndex - 1);
    });

    nextBtn.addEventListener("click", () => {
        if (currentIndex < questions.length - 1) {
            renderQuestion(currentIndex + 1);
        } else {
            openConfirmModal();
        }
    });

    submitBtn.addEventListener("click", openConfirmModal);

    function openConfirmModal() {
        answeredCountEl.textContent = Object.keys(answers).length;
        totalCountEl.textContent = questions.length;
        confirmModal.style.display = "flex";
    }

    cancelSubmit.addEventListener("click", () => {
        confirmModal.style.display = "none";
    });

    confirmSubmit.addEventListener("click", () => {
        confirmModal.style.display = "none";
        submitQuiz(false);
    });

    function submitQuiz(autoSubmitted) {
        if (submitted) return;
        submitted = true;
        if (timer) timer.stop();

        nextBtn.disabled = true;
        prevBtn.disabled = true;
        submitBtn.disabled = true;
        submitBtn.textContent = autoSubmitted ? "Time's up — submitting..." : "Submitting...";

        const timeTaken = timer ? timer.getElapsed() : 0;

        fetch("/api/quiz/submit", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category, answers, time_taken: timeTaken }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.result_id) {
                    window.location.href = `/result/${data.result_id}`;
                } else {
                    alert("Something went wrong submitting your quiz. Please try again.");
                    submitted = false;
                    submitBtn.disabled = false;
                }
            })
            .catch(() => {
                alert("Network error while submitting. Please try again.");
                submitted = false;
                submitBtn.disabled = false;
            });
    }

    // Warn before leaving an in-progress quiz
    window.addEventListener("beforeunload", (e) => {
        if (!submitted && questions.length) {
            e.preventDefault();
            e.returnValue = "";
        }
    });
});
