// Supa Voice Cloner - Main JavaScript

// Smooth scroll to generate section
function scrollToGenerate() {
    const generateSection = document.getElementById('generate-section');
    if (generateSection) {
        generateSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('#voice-cloner-form');
    const fileInput = document.querySelector('#voice_file');
    const fileLabel = document.querySelector('.file-label');
    const fileName = document.querySelector('.file-name');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const results = document.getElementById('results');
    const alertBox = document.querySelector('.alert');
    const progressBar = document.querySelector('.progress-bar');
    
    // Update file name display when file is selected
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            fileName.textContent = this.files[0].name;
            fileLabel.classList.add('has-file');
        } else {
            fileName.textContent = 'No file selected';
            fileLabel.classList.remove('has-file');
        }
    });
    
    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Hide previous alerts and results
        hideAlert();
        hideResults();
        
        // Hide the submit button to prevent multiple clicks
        const submitButton = this.querySelector('button[type="submit"]');
        submitButton.style.display = 'none';
        
        // Show loading indicator
        loadingSpinner.style.display = 'block';
        
        // Start progress bar animation
        simulateProgress();
        
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            // Hide loading indicator
            loadingSpinner.style.display = 'none';
            
            // Show the submit button again
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.style.display = 'block';
            
            if (response.ok) {
                // Show success message
                showAlert('Voice cloning completed successfully!', 'success');
                
                // Show results section
                showResults();
                
                // Set audio source
                const audioPlayer = document.getElementById('generated-audio');
                audioPlayer.src = data.generated_voice_path;
                
                // Set download link
                const downloadLink = document.getElementById('download-link');
                downloadLink.href = data.generated_voice_path;
                
                // Add filename to download
                const pathParts = data.generated_voice_path.split('/');
                const filename = pathParts[pathParts.length - 1];
                downloadLink.setAttribute('download', filename || 'cloned-voice.wav');
                
                // Scroll to results
                results.scrollIntoView({ behavior: 'smooth' });
            } else {
                // Show error message
                showAlert(data.error || 'An error occurred during voice cloning', 'error');
                resetProgress();
            }
        } catch (error) {
            // Hide loading indicator
            loadingSpinner.style.display = 'none';
            
            // Show the submit button again
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.style.display = 'block';
            
            // Show error message
            showAlert('An unexpected error occurred', 'error');
            console.error(error);
            resetProgress();
        }
    });
    
    // Helper functions
    function showAlert(message, type) {
        alertBox.textContent = message;
        alertBox.className = 'alert';
        alertBox.classList.add(`alert-${type}`);
        alertBox.style.display = 'block';
    }
    
    function hideAlert() {
        alertBox.style.display = 'none';
    }
    
    function showResults() {
        results.classList.add('show');
    }
    
    function hideResults() {
        results.classList.remove('show');
    }
    
    // Simulate progress for better user experience
    function simulateProgress() {
        resetProgress();
        let width = 0;
        const interval = setInterval(() => {
            if (width >= 90) {
                clearInterval(interval);
            } else {
                width += Math.random() * 10;
                if (width > 90) width = 90;
                progressBar.style.width = width + '%';
            }
        }, 500);
    }
    
    function resetProgress() {
        progressBar.style.width = '0%';
    }
    
    // Easter egg - voice wave animation when hovering over header
    const header = document.querySelector('header');
    header.addEventListener('mousemove', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const waves = document.querySelectorAll('.wave-path');
        
        waves.forEach((wave, index) => {
            const factor = (index + 1) * 5;
            const offset = (x / rect.width) * factor - factor / 2;
            wave.style.transform = `translateX(${offset}px)`;
        });
    });
});
