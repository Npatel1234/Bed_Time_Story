document.addEventListener('DOMContentLoaded', () => {
    const premiseSelect = document.getElementById('premise');
    const ttsToggle = document.getElementById('tts-toggle');
    const startBtn = document.getElementById('start-btn');
    const resetBtn = document.getElementById('reset-btn');
    const storyContainer = document.getElementById('story-container');
    const choicesContainer = document.getElementById('choices-container');
    const audioPlayer = document.getElementById('audio-player');
    const loadingOverlay = document.getElementById('loading-overlay');

    function showLoading() {
        loadingOverlay.style.display = 'flex';
    }

    function hideLoading() {
        loadingOverlay.style.display = 'none';
    }

    function updateStory(data) {
        storyContainer.innerHTML = data.chat_output.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        storyContainer.scrollTop = storyContainer.scrollHeight;

        choicesContainer.innerHTML = '';
        data.choices.forEach(choice => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition';
            btn.textContent = choice;
            btn.addEventListener('click', () => makeChoice(choice));
            choicesContainer.appendChild(btn);
        });

        if (data.audio) {
            audioPlayer.src = `data:audio/mp3;base64,${data.audio}`;
            audioPlayer.play().catch(e => console.error('Audio playback error:', e));
        } else {
            audioPlayer.src = '';
        }
    }

    async function startStory() {
        showLoading();
        const premise = premiseSelect.value;
        const ttsEnabled = ttsToggle.checked;
        try {
            const response = await fetch('/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ premise, tts_enabled: ttsEnabled })
            });
            const data = await response.json();
            updateStory(data);
        } catch (error) {
            storyContainer.innerHTML = 'Error starting story. Please try again.';
            console.error(error);
        } finally {
            hideLoading();
        }
    }

    async function makeChoice(choice) {
        showLoading();
        const premise = premiseSelect.value;
        const ttsEnabled = ttsToggle.checked;
        try {
            const response = await fetch('/choice', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ premise, choice, tts_enabled: ttsEnabled })
            });
            const data = await response.json();
            if (response.ok) {
                updateStory(data);
            } else {
                storyContainer.innerHTML = 'Error processing choice. Please try again.';
            }
        } catch (error) {
            storyContainer.innerHTML = 'Error processing choice. Please try again.';
            console.error(error);
        } finally {
            hideLoading();
        }
    }

    startBtn.addEventListener('click', startStory);
    resetBtn.addEventListener('click', startStory);
});