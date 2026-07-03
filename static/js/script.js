/* script.js — global site behaviour: mobile nav toggle, flash auto-dismiss */

document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("open");
        });
    }

    // Auto-dismiss flash messages after 4 seconds
    document.querySelectorAll(".flash").forEach((el) => {
        setTimeout(() => {
            el.style.transition = "opacity 0.4s ease";
            el.style.opacity = "0";
            setTimeout(() => el.remove(), 400);
        }, 4000);
    });
});
