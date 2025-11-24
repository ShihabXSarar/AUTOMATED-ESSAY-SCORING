document.addEventListener('DOMContentLoaded', () => {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const clearBtn = document.getElementById('clearBtn');
    const essayInput = document.getElementById('essayInput');
    const scoreValue = document.getElementById('scoreValue');
    const scoreCard = document.querySelector('.score-card');
    const btnLoader = document.getElementById('btnLoader');
    const btnText = document.querySelector('.btn-text');

    analyzeBtn.addEventListener('click', async () => {
        const essay = essayInput.value.trim();

        if (!essay) {
            alert('Please enter an essay to analyze.');
            return;
        }

        // Show loading state
        setLoading(true);

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ essay }),
            });

            const data = await response.json();

            if (response.ok) {
                // Animate score
                animateScore(data.score);
                scoreCard.classList.add('active');
            } else {
                alert('Error: ' + (data.error || 'Something went wrong'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to connect to the server.');
        } finally {
            setLoading(false);
        }
    });

    clearBtn.addEventListener('click', () => {
        essayInput.value = '';
        scoreValue.textContent = '0';
        scoreCard.classList.remove('active');
    });

    function setLoading(isLoading) {
        analyzeBtn.disabled = isLoading;
        if (isLoading) {
            btnText.style.display = 'none';
            btnLoader.style.display = 'block';
        } else {
            btnText.style.display = 'block';
            btnLoader.style.display = 'none';
        }
    }

    function animateScore(targetScore) {
        let currentScore = 0;
        const duration = 1000; // 1 second
        const startTime = performance.now();
        const startScore = 0;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic function
            const ease = 1 - Math.pow(1 - progress, 3);

            currentScore = startScore + (targetScore - startScore) * ease;
            scoreValue.textContent = currentScore.toFixed(1);

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }
});
