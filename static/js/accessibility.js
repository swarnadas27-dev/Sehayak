/**
 * SEHAYAK (सहायक) - Accessibility & Dyslexia Controller (WCAG 2.1 AA/AAA)
 * Manages typography (Lexend, OpenDyslexic), reading ruler focus guide,
 * Irlen syndrome color overlay filters, TTS pacing sliders, and audio feedback.
 */

(function () {
    const STORAGE_KEY = "sehayak_a11y_prefs_v2";

    const defaultPrefs = {
        fontFamily: "font-lexend",
        theme: "theme-soft-cream",
        fontSize: 16,
        lineHeight: 1.65,
        letterSpacing: 0.04,
        colorTint: "tint-none",
        rulerActive: false,
        rulerHeight: 48,
        ttsRate: 0.90,
        ttsPitch: 1.0
    };

    function loadPrefs() {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? { ...defaultPrefs, ...JSON.parse(saved) } : defaultPrefs;
        } catch (e) {
            return defaultPrefs;
        }
    }

    function savePrefs(prefs) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
        } catch (e) {
            console.warn("Could not save accessibility preferences:", e);
        }
    }

    // Pleasant Web Audio Chime (Zero external files needed)
    window.playPleasantChime = function () {
        try {
            const AudioCtx = window.AudioContext || window.webkitAudioContext;
            if (!AudioCtx) return;
            const ctx = new AudioCtx();
            const now = ctx.currentTime;

            // Two-tone gentle harmonic chime (C5 -> G5)
            const osc1 = ctx.createOscillator();
            const osc2 = ctx.createOscillator();
            const gainNode = ctx.createGain();

            osc1.type = "sine";
            osc1.frequency.setValueAtTime(523.25, now); // C5
            osc1.frequency.exponentialRampToValueAtTime(783.99, now + 0.18); // G5

            osc2.type = "triangle";
            osc2.frequency.setValueAtTime(659.25, now); // E5

            gainNode.gain.setValueAtTime(0.12, now);
            gainNode.gain.exponentialRampToValueAtTime(0.001, now + 0.45);

            osc1.connect(gainNode);
            osc2.connect(gainNode);
            gainNode.connect(ctx.destination);

            osc1.start(now);
            osc2.start(now);
            osc1.stop(now + 0.45);
            osc2.stop(now + 0.45);
        } catch (err) {
            // Audio context not allowed or blocked
        }
    };

    function applyPrefs(prefs) {
        const body = document.body;

        // Apply Font Family
        body.classList.remove("font-lexend", "font-opendyslexic", "font-sans");
        body.classList.add(prefs.fontFamily);

        // Apply Theme
        body.classList.remove(
            "theme-soft-cream",
            "theme-pastel-yellow",
            "theme-pastel-blue",
            "theme-high-contrast",
            "theme-clean-white"
        );
        body.classList.add(prefs.theme);

        // Apply Color Tint Overlay (Irlen Syndrome)
        body.classList.remove("tint-rose", "tint-aqua", "tint-yellow", "tint-lavender");
        if (prefs.colorTint && prefs.colorTint !== "tint-none") {
            body.classList.add(prefs.colorTint);
        }

        // Apply Reading Ruler
        if (prefs.rulerActive) {
            body.classList.add("ruler-active");
        } else {
            body.classList.remove("ruler-active");
        }

        // Set CSS Root Variables
        document.documentElement.style.setProperty("--font-size-base", `${prefs.fontSize}px`);
        document.documentElement.style.setProperty("--line-height-base", prefs.lineHeight);
        document.documentElement.style.setProperty("--letter-spacing-base", `${prefs.letterSpacing}em`);

        // Propagate TTS variables to window instance
        if (window.sehayakTTS) {
            window.sehayakTTS.userRate = prefs.ttsRate;
            window.sehayakTTS.userPitch = prefs.ttsPitch;
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        const prefs = loadPrefs();
        applyPrefs(prefs);

        // Set up Reading Ruler element if not already in DOM
        let ruler = document.getElementById("dyslexia-reading-ruler");
        if (!ruler) {
            ruler = document.createElement("div");
            ruler.id = "dyslexia-reading-ruler";
            document.body.appendChild(ruler);
        }

        let tintOverlay = document.getElementById("color-tint-overlay");
        if (!tintOverlay) {
            tintOverlay = document.createElement("div");
            tintOverlay.id = "color-tint-overlay";
            document.body.appendChild(tintOverlay);
        }

        // Track cursor position for reading ruler
        window.addEventListener("mousemove", (e) => {
            if (prefs.rulerActive && ruler) {
                const height = prefs.rulerHeight || 48;
                ruler.style.top = `${e.clientY - height / 2}px`;
            }
        });

        // Toggle Toolbar Panel
        const toggleBtn = document.getElementById("a11y-toggle-btn");
        const panel = document.getElementById("a11y-drawer-panel");
        const closeBtn = document.getElementById("a11y-close-btn");

        if (toggleBtn && panel) {
            toggleBtn.addEventListener("click", () => {
                const isOpen = panel.classList.toggle("open");
                toggleBtn.setAttribute("aria-expanded", isOpen);
            });
        }

        if (closeBtn && panel) {
            closeBtn.addEventListener("click", () => {
                panel.classList.remove("open");
                if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
            });
        }

        // Reading Ruler Toggle Button
        const rulerToggleBtn = document.getElementById("ruler-toggle-btn");
        if (rulerToggleBtn) {
            if (prefs.rulerActive) rulerToggleBtn.classList.add("active");
            rulerToggleBtn.addEventListener("click", () => {
                prefs.rulerActive = !prefs.rulerActive;
                rulerToggleBtn.classList.toggle("active", prefs.rulerActive);
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        }

        // Color Tint Overlay Buttons
        const tintBtns = document.querySelectorAll("[data-tint-option]");
        tintBtns.forEach((btn) => {
            const tintVal = btn.getAttribute("data-tint-option");
            if (tintVal === prefs.colorTint) btn.classList.add("active");

            btn.addEventListener("click", () => {
                tintBtns.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");
                prefs.colorTint = tintVal;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        });

        // Font Family Buttons
        const fontBtns = document.querySelectorAll("[data-font-option]");
        fontBtns.forEach((btn) => {
            const fontVal = btn.getAttribute("data-font-option");
            if (fontVal === prefs.fontFamily) btn.classList.add("active");

            btn.addEventListener("click", () => {
                fontBtns.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");
                prefs.fontFamily = fontVal;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        });

        // Theme Buttons
        const themeBtns = document.querySelectorAll("[data-theme-option]");
        themeBtns.forEach((btn) => {
            const themeVal = btn.getAttribute("data-theme-option");
            if (themeVal === prefs.theme) btn.classList.add("active");

            btn.addEventListener("click", () => {
                themeBtns.forEach((b) => b.classList.remove("active"));
                btn.classList.add("active");
                prefs.theme = themeVal;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        });

        // Font Size Slider
        const fontSizeSlider = document.getElementById("font-size-slider");
        const fontSizeVal = document.getElementById("font-size-val");
        if (fontSizeSlider) {
            fontSizeSlider.value = prefs.fontSize;
            if (fontSizeVal) fontSizeVal.textContent = `${prefs.fontSize}px`;

            fontSizeSlider.addEventListener("input", (e) => {
                prefs.fontSize = parseInt(e.target.value);
                if (fontSizeVal) fontSizeVal.textContent = `${prefs.fontSize}px`;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        }

        // Line Spacing Slider
        const lineSpacingSlider = document.getElementById("line-spacing-slider");
        const lineSpacingVal = document.getElementById("line-spacing-val");
        if (lineSpacingSlider) {
            lineSpacingSlider.value = prefs.lineHeight;
            if (lineSpacingVal) lineSpacingVal.textContent = `${prefs.lineHeight}x`;

            lineSpacingSlider.addEventListener("input", (e) => {
                prefs.lineHeight = parseFloat(e.target.value);
                if (lineSpacingVal) lineSpacingVal.textContent = `${prefs.lineHeight}x`;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        }

        // Letter Spacing Slider
        const letterSpacingSlider = document.getElementById("letter-spacing-slider");
        const letterSpacingVal = document.getElementById("letter-spacing-val");
        if (letterSpacingSlider) {
            letterSpacingSlider.value = prefs.letterSpacing;
            if (letterSpacingVal) letterSpacingVal.textContent = `${prefs.letterSpacing}em`;

            letterSpacingSlider.addEventListener("input", (e) => {
                prefs.letterSpacing = parseFloat(e.target.value);
                if (letterSpacingVal) letterSpacingVal.textContent = `${prefs.letterSpacing}em`;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        }

        // TTS Rate Slider
        const ttsRateSlider = document.getElementById("tts-rate-slider");
        const ttsRateVal = document.getElementById("tts-rate-val");
        if (ttsRateSlider) {
            ttsRateSlider.value = prefs.ttsRate;
            if (ttsRateVal) ttsRateVal.textContent = `${prefs.ttsRate}x`;

            ttsRateSlider.addEventListener("input", (e) => {
                prefs.ttsRate = parseFloat(e.target.value);
                if (ttsRateVal) ttsRateVal.textContent = `${prefs.ttsRate}x`;
                applyPrefs(prefs);
                savePrefs(prefs);
            });
        }

        // Reset Button
        const resetBtn = document.getElementById("a11y-reset-btn");
        if (resetBtn) {
            resetBtn.addEventListener("click", () => {
                Object.assign(prefs, defaultPrefs);
                applyPrefs(prefs);
                savePrefs(prefs);
                location.reload();
            });
        }
    });
})();
