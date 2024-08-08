// INFINITE CAROUSEL
document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.infinite-carousel');
    carousels.forEach(carousel => {
        // get the inner div of each carousel
        const carouselInner = carousel.querySelector('.carousel-inner');
        // get the images from the carousel
        const carouselContent = Array.from(carouselInner.children);
        // duplicate the content
        carouselContent.forEach(item => {
            const duplicatedItem = item.cloneNode(true);
            carouselInner.appendChild(duplicatedItem);
        });
        // add animation
        carouselInner.style.animation = `move 40s linear infinite`;
    });
})

// Visible/Invisible password
document.addEventListener('DOMContentLoaded', function() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
  
    passwordToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            const inputGroup = toggle.closest('.input-group');
            if (inputGroup) {
                const passwordField = inputGroup.querySelector('.password');
                if (passwordField) {
                    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
                    passwordField.setAttribute('type', type);
  
                    const toggleText = toggle.querySelector('.showPasswordToggle');
                    if (toggleText) {
                        if (type === 'password') {
                            toggleText.textContent = 'Show';
                            toggleText.style.color = 'white';
                        } else {
                            toggleText.textContent = 'Hide';
                            toggleText.style.color = '#FFCC00';
                        }
                    }
                }
            }
        });
    });
});

// MESSAGES
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        let messageContainer = document.getElementById('message-container');
        if (messageContainer) {
            messageContainer.style.display = 'none';
        }
    }, 5000);
});

// CAROUSEL

function showSlide(carouselId, index) {
    const carousel = document.getElementById(`carousel${carouselId}`);
    
    if (!carousel) {
        console.warn(`Carousel with ID carousel${carouselId} not found.`);
        return;
    }
    
    const slides = carousel.querySelectorAll('.carousel_item');
    
    if (slides.length === 0) return;

    const newIndex = (index + slides.length) % slides.length;
    const offset = -index * 100;
    carousel.querySelector('.carousel_inner').style.transform = `translateX(${offset}%)`;

    slides.forEach((slide, idx) => slide.classList.toggle('active', idx === newIndex));
}

// Function to show the previous slide
function prevSlide(carouselId) {
    const carousel = document.getElementById(`carousel${carouselId}`);
    
    if (!carousel) {
        console.warn(`Carousel with ID carousel${carouselId} not found.`);
        return;
    }
    
    const slides = carousel.querySelectorAll('.carousel_item');
    
    if (slides.length === 0) return;

    const activeSlide = Array.from(slides).findIndex(slide => slide.classList.contains('active'));
    const newIndex = (activeSlide - 1 + slides.length) % slides.length;

    showSlide(carouselId, newIndex);
}

function nextSlide(carouselId) {
    const carousel = document.getElementById(`carousel${carouselId}`);
    
    if (!carousel) {
        console.warn(`Carousel with ID carousel${carouselId} not found.`);
        return;
    }
    
    const slides = carousel.querySelectorAll('.carousel_item');
    
    if (slides.length === 0) return;

    const activeSlide = Array.from(slides).findIndex(slide => slide.classList.contains('active'));
    const newIndex = (activeSlide + 1) % slides.length;

    showSlide(carouselId, newIndex);
}

document.addEventListener('DOMContentLoaded', () => {
    const carousels = document.querySelectorAll('.carousel');
    
    carousels.forEach(carousel => {
        const slides = carousel.querySelectorAll('.carousel_item');
        if (slides.length > 0) {
            showSlide(carousel.id.replace('carousel', ''), 0);
        }
    });
});


// COUNTDOWN

document.addEventListener('DOMContentLoaded', function() {
    function parseCustomDate(dateStr, timeStr) {
        if (!dateStr || !timeStr) {
            console.error('Invalid date or time string');
            return new Date();
        }

        // Create a Date object from custom date and time strings
        const dateParts = dateStr.split(' ');
        const timeParts = timeStr.split(' ');
        
        // Month abbreviations
        const months = {
            'Jan.': 0, 'Feb.': 1, 'Mar.': 2, 'Apr.': 3, 'May': 4, 'Jun.': 5,
            'Jul.': 6, 'Aug.': 7, 'Sep.': 8, 'Oct.': 9, 'Nov.': 10, 'Dec.': 11
        };
        
        const month = months[dateParts[0]];
        const day = parseInt(dateParts[1].replace(',', ''), 10);
        const year = parseInt(dateParts[2], 10);
        
        let [hours, minutes] = timeParts[0].split(':').map(Number);
        const ampm = timeParts[1].toLowerCase();
        
        if (ampm === 'p.m.' && hours < 12) {
            hours += 12;
        } else if (ampm === 'a.m.' && hours === 12) {
            hours = 0;
        }
        
        return new Date(year, month, day, hours, minutes);
    }
    
    function updateCountdown(eventId, targetDate) {
        const countdownElement = document.getElementById(`countdown-${eventId}`);
        if (!countdownElement) return;
        const countdownDate = targetDate.getTime();
        
        function calculateCountdown() {
            const now = new Date().getTime();
            const distance = countdownDate - now;
            
            if (distance < 0) {
                countdownElement.innerHTML = "Event has passed";
                countdownElement.style.color = 'red';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((distance % (1000 * 60)) / 1000);
            
            countdownElement.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
        }
        
        setInterval(calculateCountdown, 1000);
    }

    const events = document.querySelectorAll('.event-time .event-item[id^="countdown-"]');
    events.forEach(event => {
        const eventId = event.id.split('-')[1];
        const eventDateStr = event.getAttribute('data-date');
        const eventTimeStr = event.getAttribute('data-time');
        
        if (eventDateStr && eventTimeStr) {
            const targetDate = parseCustomDate(eventDateStr, eventTimeStr);
            updateCountdown(eventId, targetDate);
        } else {
            console.error(`Missing date or time for event with ID ${eventId}`);
        }
    });
});