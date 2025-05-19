document.getElementById('story-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const formData = new FormData(this);
    const storyOutput = document.getElementById('story-output');
    const storyText = document.getElementById('story-text');
    const audioPlayer = document.getElementById('audio-player');
    const storyAudio = document.getElementById('story-audio');
    
    storyText.innerHTML = 'Generating your story...';
    storyOutput.style.display = 'block';
    audioPlayer.style.display = 'none';
    
    try {
        const response = await fetch('/generate_story', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            storyText.innerHTML = `Error: ${data.error}`;
            audioPlayer.style.display = 'none';
        } else {
            storyText.innerHTML = data.story.replace(/\n/g, '<br>');
            if (data.audio_url) {
                storyAudio.src = data.audio_url;
                audioPlayer.style.display = 'block';
            }
        }
    } catch (error) {
        storyText.innerHTML = 'Error: Could not connect to the server.';
        audioPlayer.style.display = 'none';
    }
});