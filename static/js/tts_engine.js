/**
 * SEHAYAK (सहायक) - Bilingual Text-to-Speech (TTS) Engine
 * Implements accessible Web Speech API for reading aloud student content
 * in Hindi (hi-IN) and English (en-IN/en-US) with synchronized visual tracking
 * and user-controlled pacing.
 */

class SehayakTTS {
    constructor() {
        this.synth = window.speechSynthesis;
        this.currentUtterance = null;
        this.activeElement = null;
        this.voices = [];
        this.userRate = 0.90;
        this.userPitch = 1.0;

        if (this.synth) {
            this.loadVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = () => this.loadVoices();
            }
        }
    }

    loadVoices() {
        if (!this.synth) return;
        this.voices = this.synth.getVoices();
    }

    getBestVoice(lang = "en") {
        if (!this.voices || this.voices.length === 0) {
            this.loadVoices();
        }

        if (lang === "hi") {
            const hiVoice = this.voices.find(v => v.lang.startsWith("hi") || v.lang.includes("HI"));
            if (hiVoice) return hiVoice;
        }

        // English preference: Indian English (en-IN), otherwise en-GB / en-US
        const inVoice = this.voices.find(v => v.lang === "en-IN");
        if (inVoice) return inVoice;

        return this.voices.find(v => v.lang.startsWith("en")) || this.voices[0];
    }

    speak(text, element = null, lang = "en") {
        if (!this.synth) {
            alert("Speech synthesis is not supported on this browser.");
            return;
        }

        // Cancel previous speech if running
        this.stop();

        if (!text || text.trim() === "") return;

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = lang === "hi" ? "hi-IN" : "en-IN";
        utterance.rate = this.userRate || 0.90; // User controlled pace
        utterance.pitch = this.userPitch || 1.0;

        const voice = this.getBestVoice(lang);
        if (voice) {
            utterance.voice = voice;
        }

        if (element) {
            this.activeElement = element;
            element.classList.add("tts-speaking");
        }

        utterance.onend = () => {
            this.clearHighlight();
        };

        utterance.onerror = (e) => {
            console.warn("Speech synthesis notice:", e);
            this.clearHighlight();
        };

        this.currentUtterance = utterance;
        this.synth.speak(utterance);
    }

    stop() {
        if (this.synth) {
            this.synth.cancel();
        }
        this.clearHighlight();
    }

    clearHighlight() {
        if (this.activeElement) {
            this.activeElement.classList.remove("tts-speaking");
            this.activeElement = null;
        }
    }
}

// Global Singleton Instance
window.sehayakTTS = new SehayakTTS();

document.addEventListener("DOMContentLoaded", function () {
    // Attach listener to any element with .tts-btn or data-tts
    document.body.addEventListener("click", function (e) {
        const ttsBtn = e.target.closest(".tts-btn");
        if (ttsBtn) {
            e.preventDefault();
            const targetId = ttsBtn.getAttribute("data-target-id");
            const lang = ttsBtn.getAttribute("data-lang") || "en";

            let textToSpeak = "";
            let targetEl = null;

            if (targetId) {
                targetEl = document.getElementById(targetId);
                if (targetEl) {
                    textToSpeak = targetEl.innerText || targetEl.textContent;
                }
            } else if (ttsBtn.hasAttribute("data-speak-text")) {
                textToSpeak = ttsBtn.getAttribute("data-speak-text");
                targetEl = ttsBtn;
            }

            if (window.sehayakTTS.synth && window.sehayakTTS.synth.speaking) {
                window.sehayakTTS.stop();
            } else {
                window.sehayakTTS.speak(textToSpeak, targetEl, lang);
            }
        }
    });
});
