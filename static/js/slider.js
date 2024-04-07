// Получаем все необходимые элементы
const sliderContainer = document.querySelector('.slider-container');
const slides = document.querySelectorAll('.slide');
const prevButton = document.querySelector('.prev-slide');
const nextButton = document.querySelector('.next-slide');

let currentSlide = 0;

// Функция для показа определенного слайда
function showSlide(slideIndex) {
    // Скрываем все слайды
    slides.forEach(slide => {
        slide.style.display = 'none';
    });
    // Показываем выбранный слайд
    slides[slideIndex].style.display = 'block';
}

// Показываем первый слайд при загрузке страницы
showSlide(currentSlide);

// Обработчик для кнопки "Предыдущий слайд"
prevButton.addEventListener('click', () => {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
});

// Обработчик для кнопки "Следующий слайд"
nextButton.addEventListener('click', () => {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
});