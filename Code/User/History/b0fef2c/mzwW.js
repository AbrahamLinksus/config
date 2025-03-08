document.addEventListener("scroll", function () {
    let text = document.querySelector(".section-1-text");
    let position = text.getBoundingClientRect().top;
    let windowHeight = window.innerHeight;

    if (position < windowHeight * 0.75) {
        text.classList.add("hidden"); // Apply fade effect
    } else {
        text.classList.remove("hidden"); // Reset when scrolling back up
    }
});
