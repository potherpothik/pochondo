/** @odoo-module **/

document.addEventListener("DOMContentLoaded", () => {
    const revealNodes = document.querySelectorAll(".shop-suite-reveal");
    if (!revealNodes.length) {
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        },
        {
            threshold: 0.2,
        }
    );

    revealNodes.forEach((node) => observer.observe(node));
});
