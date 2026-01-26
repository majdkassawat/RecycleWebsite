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

    // Supabase configuration - will be set from admin page
    const getConfig = () => {
        try {
            return JSON.parse(localStorage.getItem('tadweer_supabase_config') || '{}');
        } catch {
            return {};
        }
    };

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

    // Generate tracking ID
    const generateTrackingId = () => {
        const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
        let id = 'TDW-';
        for (let i = 0; i < 6; i++) {
            id += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return id;
    };

    // Submit feedback to Supabase
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
        const trackingId = generateTrackingId();
        
        const data = {
            tracking_id: trackingId,
            name: formData.get('name') || 'Anonymous',
            email: formData.get('email') || '',
            category: formData.get('category'),
            suggestion: formData.get('suggestion'),
            status: 'new',
            page_url: window.location.href
        };

        // Store locally for tracking
        const stored = JSON.parse(localStorage.getItem('tadweer_feedback') || '[]');
        stored.push({
            ...data,
            id: trackingId,
            date: new Date().toLocaleDateString()
        });
        localStorage.setItem('tadweer_feedback', JSON.stringify(stored.slice(-20)));

        // Try to submit to Supabase
        const config = getConfig();
        let submitted = false;
        
        if (config.url && config.key) {
            try {
                const response = await fetch(`${config.url}/rest/v1/suggestions`, {
                    method: 'POST',
                    headers: {
                        'apikey': config.key,
                        'Authorization': `Bearer ${config.key}`,
                        'Content-Type': 'application/json',
                        'Prefer': 'return=minimal'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.ok || response.status === 201) {
                    submitted = true;
                }
            } catch (error) {
                console.error('Supabase submission failed:', error);
            }
        }

        // Fallback: open email if Supabase not configured or failed
        if (!submitted) {
            const emailSubject = encodeURIComponent(`[${data.category}] Website Suggestion - ${trackingId}`);
            const emailBody = encodeURIComponent(
                `Tracking ID: ${trackingId}\n` +
                `Category: ${data.category}\n` +
                `From: ${data.name}${data.email ? ' (' + data.email + ')' : ''}\n` +
                `Date: ${new Date().toISOString()}\n` +
                `Page: ${window.location.href}\n\n` +
                `--- Suggestion ---\n\n` +
                `${data.suggestion}\n\n` +
                `--- End ---`
            );
            window.location.href = `mailto:tadweer.sy@gmail.com?subject=${emailSubject}&body=${emailBody}`;
        }

        // Show success message
        document.getElementById('trackingIdDisplay').textContent = trackingId;
        formView.classList.add('feedback-hidden');
        successView.classList.remove('feedback-hidden');
        
        // Reset form
        form.reset();
        if (charCount) charCount.textContent = '0';
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    });

    // Track existing feedback - check both local and Supabase
    trackForm?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const trackId = document.getElementById('trackingIdInput').value.trim().toUpperCase();
        
        if (!trackId) return;

        const resultContent = document.getElementById('trackResultContent');
        resultContent.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Checking...';
        trackResult.classList.remove('feedback-hidden');

        // Check local storage first
        const stored = JSON.parse(localStorage.getItem('tadweer_feedback') || '[]');
        let found = stored.find(f => f.tracking_id === trackId || f.id === trackId);

        // Try Supabase if configured and not found locally
        const config = getConfig();
        if (config.url && config.key) {
            try {
                const response = await fetch(
                    `${config.url}/rest/v1/suggestions?tracking_id=eq.${trackId}&select=tracking_id,category,status,created_at`,
                    {
                        headers: {
                            'apikey': config.key,
                            'Authorization': `Bearer ${config.key}`
                        }
                    }
                );
                
                if (response.ok) {
                    const results = await response.json();
                    if (results.length > 0) {
                        found = results[0];
                        found.date = new Date(found.created_at).toLocaleDateString();
                    }
                }
            } catch (error) {
                console.error('Supabase lookup failed:', error);
            }
        }

        if (found) {
            const statusLabels = {
                'new': 'Received - Awaiting Review',
                'reviewing': 'Under Review',
                'implemented': '✅ Implemented',
                'declined': 'Not Planned'
            };
            resultContent.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <h4>Suggestion Found</h4>
                <p><strong>ID:</strong> ${found.tracking_id || found.id}</p>
                <p><strong>Category:</strong> ${found.category}</p>
                <p><strong>Submitted:</strong> ${found.date}</p>
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
    });
})();

