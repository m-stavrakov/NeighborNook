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