const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const navLinks = document.querySelectorAll('.nav-links li');

    burger.addEventListener('click', () => {
        // Toggle Nav
        nav.classList.toggle('nav-active');

        // Animate Links
        navLinks.forEach((link, index) => {
            if (link.style.animation) {
                link.style.animation = '';
            } else {
                link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
            }
        });

        // Burger Animation
        burger.classList.toggle('toggle');
    });
}

navSlide();

// Initialize AOS
AOS.init({
    duration: 1000,
    once: true
});

// Back to Top Button
const backToTopButton = document.getElementById("backToTop");

window.onscroll = function() {
    scrollFunction();
    highlightNav();
};

function scrollFunction() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        backToTopButton.style.display = "block";
    } else {
        backToTopButton.style.display = "none";
    }
}

backToTopButton.addEventListener("click", function() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
});

// Highlight Active Nav Link
const sections = document.querySelectorAll("section");
const navLi = document.querySelectorAll(".nav-links li a");

function highlightNav() {
    let current = "";
    sections.forEach((section) => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        // Offset for fixed header
        if (pageYOffset >= (sectionTop - sectionHeight / 3)) {
            current = section.getAttribute("id");
        }
    });

    navLi.forEach((a) => {
        a.classList.remove("active-section");
        if (a.getAttribute("href").includes(current) && current !== "") {
            a.classList.add("active-section");
        }
    });
}

// Simple slider for Events page
(function initEventsSlider() {
    const slider = document.querySelector(".events-slider");
    if (!slider) return;

    const slides = Array.from(slider.querySelectorAll(".slide"));
    const dots = Array.from(slider.querySelectorAll(".dot"));
    const counter = slider.querySelector(".slide-counter");
    const prev = document.getElementById("prevSlide");
    const next = document.getElementById("nextSlide");
    let currentIndex = slides.findIndex((slide) => slide.classList.contains("active"));
    let timer;

    if (currentIndex === -1) currentIndex = 0;

    const showSlide = (index) => {
        if (!slides.length) return;
        const newIndex = (index + slides.length) % slides.length;
        slides.forEach((slide, idx) => slide.classList.toggle("active", idx === newIndex));
        dots.forEach((dot, idx) => dot.classList.toggle("active", idx === newIndex));
        if (counter) counter.textContent = `${newIndex + 1} / ${slides.length}`;
        currentIndex = newIndex;
        resetTimer();
    };

    const resetTimer = () => {
        if (timer) clearInterval(timer);
        timer = setInterval(() => showSlide(currentIndex + 1), 7000);
    };

    prev?.addEventListener("click", () => showSlide(currentIndex - 1));
    next?.addEventListener("click", () => showSlide(currentIndex + 1));
    dots.forEach((dot, idx) => dot.addEventListener("click", () => showSlide(idx)));

    showSlide(currentIndex);
})();

// ===== FEEDBACK WIDGET =====
(function initFeedbackWidget() {
    const bubble = document.getElementById('feedbackBubble');
    const modal = document.getElementById('feedbackModal');
    const closeBtn = document.getElementById('feedbackClose');
    const form = document.getElementById('feedbackForm');
    const tabs = document.querySelectorAll('.feedback-tab');
    const formView = document.getElementById('feedbackFormView');
    const trackView = document.getElementById('feedbackTrackView');
    const successView = document.getElementById('feedbackSuccess');
    const trackForm = document.getElementById('trackForm');
    const trackResult = document.getElementById('trackResult');
    const charCount = document.getElementById('charCount');
    const suggestionInput = document.getElementById('feedbackSuggestion');
    
    if (!bubble || !modal) return;

    // API endpoint - uses Vercel serverless function
    const API_URL = 'https://tadweer-website.vercel.app/api/suggestions';

    // Toggle modal
    bubble.addEventListener('click', () => {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });

    const closeModal = () => {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    closeBtn?.addEventListener('click', closeModal);
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Tab switching
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const view = tab.dataset.tab;
            formView?.classList.toggle('feedback-hidden', view !== 'submit');
            trackView?.classList.toggle('feedback-hidden', view !== 'track');
            successView?.classList.add('feedback-hidden');
            trackResult?.classList.add('feedback-hidden');
        });
    });

    // Character counter
    suggestionInput?.addEventListener('input', () => {
        if (charCount) {
            charCount.textContent = suggestionInput.value.length;
        }
    });

    // Submit feedback to Vercel API
    form?.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Honeypot check - if filled, it's a bot
        const hp = document.getElementById('feedbackHp');
        if (hp && hp.value) {
            console.log('Bot detected');
            return;
        }

        const submitBtn = form.querySelector('.feedback-submit');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';

        const formData = new FormData(form);
        
        const data = {
            name: formData.get('name') || 'Anonymous',
            email: formData.get('email') || '',
            category: formData.get('category'),
            suggestion: formData.get('suggestion'),
            page_url: window.location.href
        };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (response.ok && result.tracking_id) {
                // Store locally for backup tracking
                const stored = JSON.parse(localStorage.getItem('tadweer_feedback') || '[]');
                stored.push({
                    tracking_id: result.tracking_id,
                    category: data.category,
                    date: new Date().toLocaleDateString(),
                    status: 'new'
                });
                localStorage.setItem('tadweer_feedback', JSON.stringify(stored.slice(-20)));

                // Show success
                document.getElementById('trackingIdDisplay').textContent = result.tracking_id;
                formView.classList.add('feedback-hidden');
                successView.classList.remove('feedback-hidden');
                form.reset();
                if (charCount) charCount.textContent = '0';
            } else {
                throw new Error(result.error || 'Submission failed');
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('Failed to submit. Please try again later.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        }
    });

    // Track existing feedback
    trackForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const trackId = document.getElementById('trackingIdInput').value.trim().toUpperCase();
        
        if (!trackId) return;

        const resultContent = document.getElementById('trackResultContent');
        resultContent.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
        trackResult.classList.remove('feedback-hidden');

        try {
            // Try API first
            const response = await fetch(`${API_URL}?tracking_id=${encodeURIComponent(trackId)}`);
            const results = await response.json();
            
            let found = results.length > 0 ? results[0] : null;

            // Fall back to local storage
            if (!found) {
                const stored = JSON.parse(localStorage.getItem('tadweer_feedback') || '[]');
                found = stored.find(f => f.tracking_id === trackId);
            }

            if (found) {
                const statusLabels = {
                    'new': 'Received - Awaiting Review',
                    'reviewing': 'Under Review',
                    'implemented': '✅ Implemented',
                    'declined': 'Not Planned'
                };
                const date = found.created_at 
                    ? new Date(found.created_at).toLocaleDateString()
                    : found.date || 'Unknown';
                    
                resultContent.innerHTML = `
                    <i class="fas fa-check-circle"></i>
                    <h4>Suggestion Found</h4>
                    <p><strong>ID:</strong> ${found.tracking_id}</p>
                    <p><strong>Category:</strong> ${found.category}</p>
                    <p><strong>Submitted:</strong> ${date}</p>
                    <p><strong>Status:</strong> ${statusLabels[found.status] || found.status}</p>
                `;
            } else {
                resultContent.innerHTML = `
                    <i class="fas fa-search" style="color: #888;"></i>
                    <h4>Not Found</h4>
                    <p>No suggestion found with ID: ${trackId}</p>
                    <p><small>Please check the ID and try again.</small></p>
                `;
            }
        } catch (error) {
            console.error('Tracking error:', error);
            resultContent.innerHTML = `
                <i class="fas fa-exclamation-triangle" style="color: #f57c00;"></i>
                <h4>Error</h4>
                <p>Could not check status. Please try again later.</p>
            `;
        }
    });
})();

