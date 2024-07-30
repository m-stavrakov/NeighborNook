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