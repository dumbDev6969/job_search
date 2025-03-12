cript>
    document.addEventListener("DOMContentLoaded", function () {
        const elements = document.querySelectorAll(".fade-in");

        function checkScroll() {
            elements.forEach((el) => {
                const position = el.getBoundingClientRect().top;
                if (position < window.innerHeight * 0.9) {
                    el.classList.add("show");
                }
            });
        }

        window.addEventListener("scroll", checkScroll);
        checkScroll();
    });