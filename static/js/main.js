class StoryApp {
    constructor() {
        this.premise = '';
        this.initializeElements();
        this.attachEventListeners();
    }

    initializeElements() {
        this.premiseSelect = document.getElementById('premise-select');
        this.startButton = document.getElementById('start-story');
        this.resetButton = document.getElementById('reset-story');
        this.storyContent = document.getElementById('story-content');
        this.choicesContainer = document.getElementById('choices-container');
        this.audioPlayer = document.getElementById('narration');
    }

    attachEventListeners() {
        this.startButton.addEventListener('click', () => this.startStory());
        this.resetButton.addEventListener('click', () => this.startStory());
    }

    async startStory() {
        this.premise = this.premiseSelect.value;
        try {
            const response = await fetch('/api/story/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ premise: this.premise }),
            });
            const data = await response.json();
            this.updateUI(data);
        } catch (error) {
            console.error('Error starting story:', error);
        }
    }

    async makeChoice(choice) {
        try {
            const response = await fetch('/api/story/continue', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    premise: this.premise,
                    choice: choice,
                }),
            });
            const data = await response.json();
            this.updateUI(data);
        } catch (error) {
            console.error('Error making choice:', error);
        }
    }

    updateUI(data) {
        // Update story content
        this.storyContent.innerHTML = this.formatStory(data.story);

        // Update audio player
        if (data.audio) {
            this.audioPlayer.src = data.audio;
            this.audioPlayer.play();
        }

        // Update choices
        this.choicesContainer.innerHTML = '';
        data.choices.forEach(choice => {
            const button = document.createElement('button');
            button.className = 'choice-btn';
            button.textContent = choice;
            button.addEventListener('click', () => this.makeChoice(choice));
            this.choicesContainer.appendChild(button);
        });
    }

    formatStory(story) {
        // Convert markdown-style formatting to HTML
        return story
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new StoryApp();
}); 