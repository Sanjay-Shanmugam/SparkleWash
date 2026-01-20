document.addEventListener('DOMContentLoaded', () => {
    // 1. Page Loader
    window.addEventListener('load', () => {
        const loader = document.getElementById('page-loader');
        if (loader) loader.classList.add('hidden');
    });

    // 2. Scroll Animations
    const reveals = document.querySelectorAll('.reveal');
    const revealOnScroll = () => {
        const windowHeight = window.innerHeight;
        const elementVisible = 150;

        reveals.forEach((reveal) => {
            const elementTop = reveal.getBoundingClientRect().top;
            if (elementTop < windowHeight - elementVisible) {
                reveal.classList.add('active');
            }
        });
    };
    window.addEventListener('scroll', revealOnScroll);
    revealOnScroll();

    // 3. Slideshow Logic
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');

    if (slides.length > 1) {
        setInterval(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }, 5000);
    }

    // 4. Booking Slot Logic & Clock Animation
    const dateInput = document.getElementById('booking_date');
    const slotsContainer = document.getElementById('slots-container');
    const startTimeInput = document.getElementById('start_time');
    const analogClock = document.getElementById('analog-clock');
    const hourHand = document.querySelector('.hour-hand');
    const minuteHand = document.querySelector('.minute-hand');

    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.min = today;

        dateInput.addEventListener('change', async (e) => {
            const date = e.target.value;
            if (!date) return;

            slotsContainer.innerHTML = '<p style="color:var(--primary)">Checking availability...</p>';
            startTimeInput.value = '';
            if (analogClock) analogClock.classList.remove('visible');

            try {
                const response = await fetch(`/api/slots?date=${date}`);
                const slots = await response.json();

                slotsContainer.innerHTML = '';

                if (slots.length === 0) {
                    slotsContainer.innerHTML = '<p>No slots available.</p>';
                    return;
                }

                // Show clock
                if (analogClock) analogClock.classList.add('visible');

                slots.forEach(time => {
                    const btn = document.createElement('button');
                    btn.type = 'button';
                    btn.className = 'slot-btn';
                    btn.textContent = time;

                    btn.addEventListener('click', () => {
                        document.querySelectorAll('.slot-btn').forEach(b => b.classList.remove('selected'));
                        btn.classList.add('selected');
                        startTimeInput.value = time;

                        // Update Clock
                        updateClock(time);
                    });

                    slotsContainer.appendChild(btn);
                });

            } catch (err) {
                console.error('Error:', err);
                slotsContainer.innerHTML = '<p>Error loading slots.</p>';
            }
        });
    }

    function updateClock(timeStr) {
        if (!hourHand || !minuteHand) return;

        const [hours, mins] = timeStr.split(':').map(Number);

        // Calculate degrees
        // Hour hand: 360 / 12 = 30 deg per hour. Plus 0.5 deg per minute.
        const hourDeg = (hours % 12) * 30 + (mins * 0.5);
        // Minute hand: 360 / 60 = 6 deg per minute.
        const minDeg = mins * 6;

        // Add initial rotate offset if needed, CSS starts at 12 o'clock, which is 0deg.
        // But our hands css transform might need checking.
        // CSS transform-origin is bottom center.
        // 0deg is pointing UP (12 o'clock) if we style it right.

        hourHand.style.transform = `translateX(-50%) rotate(${hourDeg}deg)`;
        minuteHand.style.transform = `translateX(-50%) rotate(${minDeg}deg)`;
    }
});
