document.addEventListener("DOMContentLoaded", function () {
    const text = document.querySelector(".section-1-text");

    const observer = new IntersectionObserver(
        ([entry]) => {
            if (!entry.isIntersecting) {
                text.classList.add("hidden"); // Apply fade-out when scrolled
            } else {
                text.classList.remove("hidden"); // Reset fade effect when back in view
            }
        },
        { threshold: 0.1 } // Trigger when 10% of the text is visible
    );

    observer.observe(text);
});
const observer = new IntersectionObserver((entries) =>{
    entries.forEach(entry => {
        console.log(entry)
        if (entry.isIntersecting){
            entry.target.classList.add("show");
        } else {
            entry.target.classList.remove("show");
        }
    });
});
const hiddenElements = document.querySelectorAll(".hidden");
hiddenElements.forEach((el) => observer.observe(el));