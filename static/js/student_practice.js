/**
 * SEHAYAK (सहायक) - Student Practice Controller
 * Non-punitive, encouraging, multisensory practice questions.
 * Includes pleasant synthesizer chime, zero countdown timers, and zero negative buzzers.
 */

document.addEventListener("DOMContentLoaded", function () {
    const practiceCards = document.querySelectorAll(".practice-card");

    practiceCards.forEach((card) => {
        const options = card.querySelectorAll(".practice-option");
        const hintBtn = card.querySelector(".hint-toggle-btn");
        const hintBox = card.querySelector(".practice-hint");
        const feedbackBox = card.querySelector(".practice-feedback");
        const correctIndex = parseInt(card.getAttribute("data-correct-index"));
        const encouragingMsg = card.getAttribute("data-encouraging-msg");
        const tryAgainMsg = card.getAttribute("data-tryagain-msg");

        // Toggle Hint
        if (hintBtn && hintBox) {
            hintBtn.addEventListener("click", () => {
                const isHidden = hintBox.style.display === "none" || !hintBox.style.display;
                hintBox.style.display = isHidden ? "block" : "none";
                hintBtn.textContent = isHidden ? "Hide Visual Hint" : "Need a Visual Hint?";
            });
        }

        // Option click handling
        options.forEach((optBtn, idx) => {
            optBtn.addEventListener("click", () => {
                // Clear previous states on this card
                options.forEach(b => b.classList.remove("selected-correct", "selected-retry"));

                if (idx === correctIndex) {
                    optBtn.classList.add("selected-correct");
                    feedbackBox.className = "practice-feedback feedback-success";
                    feedbackBox.innerHTML = `
                        <div style="font-size: 1.1rem; font-weight: 700; color: #065F46; margin-bottom: 0.25rem;">
                            ${encouragingMsg}
                        </div>
                    `;
                    feedbackBox.style.display = "block";

                    // Play pleasant gentle chime
                    if (window.playPleasantChime) {
                        window.playPleasantChime();
                    }

                    // Audio reinforcement
                    const currentLang = document.documentElement.lang || "en";
                    if (window.sehayakTTS) {
                        window.sehayakTTS.speak(encouragingMsg, feedbackBox, currentLang);
                    }
                } else {
                    optBtn.classList.add("selected-retry");
                    feedbackBox.className = "practice-feedback feedback-retry";
                    feedbackBox.innerHTML = `
                        <div style="font-size: 0.95rem; font-weight: 600; color: #92400E; margin-bottom: 0.25rem;">
                            ${tryAgainMsg}
                        </div>
                    `;
                    feedbackBox.style.display = "block";
                    if (hintBox) hintBox.style.display = "block";
                }
            });
        });
    });
});
