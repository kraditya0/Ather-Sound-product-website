document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. Custom Interactive Cursor ---
    const cursor = document.getElementById("custom-cursor");
    const cursorDot = document.getElementById("custom-cursor-dot");
    
    if (cursor && cursorDot) {
        document.addEventListener("mousemove", (e) => {
            cursor.style.left = `${e.clientX}px`;
            cursor.style.top = `${e.clientY}px`;
            cursorDot.style.left = `${e.clientX}px`;
            cursorDot.style.top = `${e.clientY}px`;
        });
        
        // Add hover effects on interactive elements
        const hoverElements = document.querySelectorAll("a, button, select, input, textarea, .cursor-zoom-in");
        hoverElements.forEach(el => {
            el.addEventListener("mouseenter", () => document.body.classList.add("cursor-hover"));
            el.addEventListener("mouseleave", () => document.body.classList.remove("cursor-hover"));
        });
    }

    // --- 2. Glassmorphic Header scroll effect ---
    const header = document.getElementById("main-header");
    if (header) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 20) {
                header.classList.add("header-glass");
                header.classList.remove("border-transparent");
            } else {
                header.classList.remove("header-glass");
                header.classList.add("border-transparent");
            }
        });
    }

    // --- 3. Mobile Hamburger Overlay Menu ---
    const menuBtn = document.getElementById("menu-btn");
    const mobileOverlay = document.getElementById("mobile-overlay");
    const bar1 = document.getElementById("menu-bar-1");
    const bar2 = document.getElementById("menu-bar-2");
    const bar3 = document.getElementById("menu-bar-3");
    
    if (menuBtn && mobileOverlay) {
        menuBtn.addEventListener("click", () => {
            const isActive = mobileOverlay.classList.toggle("active");
            if (isActive) {
                // Morph bars into X
                bar1.style.transform = "rotate(45deg) translate(5px, 5px)";
                bar2.style.opacity = "0";
                bar3.style.transform = "rotate(-45deg) translate(5px, -5px)";
                document.body.style.overflow = "hidden"; // Prevent scrolling
            } else {
                // Return to normal
                bar1.style.transform = "none";
                bar2.style.opacity = "1";
                bar3.style.transform = "none";
                document.body.style.overflow = "";
            }
        });
    }

    // --- 4. Dark & Light Mode Toggle ---
    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", () => {
            const isDark = document.documentElement.classList.toggle("dark");
            localStorage.setItem("theme", isDark ? "dark" : "light");
        });
    }

    // --- 5. Flash Message slide-in & close ---
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach((msg, idx) => {
        // Stagger slide-in
        setTimeout(() => {
            msg.classList.add("show");
        }, idx * 150 + 50);
        
        // Auto-dismiss after 6s
        const autoDismiss = setTimeout(() => {
            dismissFlash(msg);
        }, 6000);

        const closeBtn = msg.querySelector(".flash-close-btn");
        if (closeBtn) {
            closeBtn.addEventListener("click", () => {
                clearTimeout(autoDismiss);
                dismissFlash(msg);
            });
        }
    });

    function dismissFlash(msg) {
        msg.style.transform = "translateX(50px)";
        msg.style.opacity = "0";
        setTimeout(() => {
            msg.remove();
        }, 500);
    }

    // --- 6. Homepage Testimonial Slider ---
    const slides = document.querySelectorAll(".testimonial-slide");
    const indicators = document.querySelectorAll("#testimonial-indicators [data-index]");
    const prevBtn = document.getElementById("prev-testimonial");
    const nextBtn = document.getElementById("next-testimonial");
    let currentSlide = 0;
    
    if (slides.length > 0) {
        function showSlide(index) {
            slides[currentSlide].classList.add("opacity-0", "pointer-events-none");
            slides[currentSlide].setAttribute("data-active", "false");
            indicators[currentSlide].classList.replace("bg-brand-gold", "bg-neutral-300");
            if (indicators[currentSlide].classList.contains("dark:bg-neutral-800")) {
                // Keep dark background if present
            } else {
                indicators[currentSlide].classList.add("dark:bg-neutral-800");
            }

            currentSlide = (index + slides.length) % slides.length;

            slides[currentSlide].classList.remove("opacity-0", "pointer-events-none");
            slides[currentSlide].setAttribute("data-active", "true");
            indicators[currentSlide].classList.remove("bg-neutral-300", "dark:bg-neutral-800");
            indicators[currentSlide].classList.add("bg-brand-gold");
        }

        if (nextBtn) nextBtn.addEventListener("click", () => showSlide(currentSlide + 1));
        if (prevBtn) prevBtn.addEventListener("click", () => showSlide(currentSlide - 1));
        
        indicators.forEach(ind => {
            ind.addEventListener("click", () => {
                showSlide(parseInt(ind.getAttribute("data-index")));
            });
        });

        // Autoplay testimonials
        setInterval(() => {
            showSlide(currentSlide + 1);
        }, 8000);
    }

    // --- 7. GSAP Premium Entrance & Scroll Animations ---
    if (typeof gsap !== "undefined") {
        gsap.registerPlugin(ScrollTrigger);

        // A. Hero entrance timelines
        const heroTl = gsap.timeline({ defaults: { ease: "power4.out" } });
        if (document.querySelector(".hero-sub")) {
            heroTl.fromTo(".hero-sub", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 1.2, delay: 0.2 })
                  .fromTo(".hero-title", { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 1.5 }, "-=1.0")
                  .fromTo(".hero-desc", { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 1.2 }, "-=1.2")
                  .fromTo(".hero-ctas", { opacity: 0, y: 10 }, { opacity: 1, y: 0, duration: 1.2 }, "-=1.0")
                  .fromTo(".hero-scroll", { opacity: 0 }, { opacity: 1, duration: 1.0 }, "-=0.6");
        }

        // B. Scroll Trigger: Featured Grid Header
        if (document.querySelector(".featured-header")) {
            gsap.from(".featured-header", {
                scrollTrigger: {
                    trigger: ".featured-header",
                    start: "top 85%"
                },
                opacity: 0,
                y: 30,
                duration: 1.2,
                ease: "power3.out"
            });
        }

        // C. Scroll Trigger: Featured Cards Stagger
        if (document.querySelectorAll(".featured-card").length > 0) {
            gsap.to(".featured-card", {
                scrollTrigger: {
                    trigger: ".featured-card",
                    start: "top 80%"
                },
                opacity: 1,
                y: 0,
                duration: 1.2,
                stagger: 0.15,
                ease: "power3.out"
            });
        }

        // D. Scroll Trigger: Why Choose Us Items
        if (document.querySelector(".why-header")) {
            gsap.from(".why-header", {
                scrollTrigger: {
                    trigger: ".why-header",
                    start: "top 85%"
                },
                opacity: 0,
                y: 30,
                duration: 1.2,
                ease: "power3.out"
            });
            
            gsap.to(".why-item", {
                scrollTrigger: {
                    trigger: ".why-item",
                    start: "top 80%"
                },
                opacity: 1,
                y: 0,
                duration: 1.2,
                stagger: 0.2,
                ease: "power3.out"
            });
        }

        // E. Scroll Trigger: Gallery Preview Grid
        if (document.querySelector(".gallery-preview-header")) {
            gsap.from(".gallery-preview-header", {
                scrollTrigger: {
                    trigger: ".gallery-preview-header",
                    start: "top 85%"
                },
                opacity: 0,
                y: 30,
                duration: 1.2,
                ease: "power3.out"
            });
            
            gsap.from("#gallery-preview-grid > div", {
                scrollTrigger: {
                    trigger: "#gallery-preview-grid",
                    start: "top 80%"
                },
                opacity: 0,
                y: 40,
                duration: 1.4,
                stagger: 0.15,
                ease: "power3.out"
            });
        }

        // F. About Page Timelines
        if (document.querySelector(".about-intro")) {
            gsap.to(".about-intro", { opacity: 1, y: 0, duration: 1.2, ease: "power3.out" });
            gsap.to(".about-media", { opacity: 1, y: 0, duration: 1.5, delay: 0.2, ease: "power3.out" });
            
            gsap.to(".timeline-item", {
                scrollTrigger: {
                    trigger: ".timeline-item",
                    start: "top 85%"
                },
                opacity: 1,
                y: 0,
                duration: 1.2,
                stagger: 0.2,
                ease: "power3.out"
            });

            gsap.to(".team-card", {
                scrollTrigger: {
                    trigger: ".team-card",
                    start: "top 85%"
                },
                opacity: 1,
                y: 0,
                duration: 1.2,
                stagger: 0.15,
                ease: "power3.out"
            });
        }

        // G. Contact Page Entrance
        if (document.querySelector(".contact-details")) {
            gsap.to(".contact-details", { opacity: 1, x: 0, duration: 1.2, ease: "power3.out" });
            gsap.to(".contact-form-wrapper", { opacity: 1, x: 0, duration: 1.2, delay: 0.1, ease: "power3.out" });
        }

    } else {
        // Fallback: If GSAP CDN is blocked/slow, make elements visible instantly
        const hiddenElements = document.querySelectorAll(
            ".featured-card, .why-item, .about-intro, .about-media, .timeline-item, .team-card, .contact-details, .contact-form-wrapper"
        );
        hiddenElements.forEach(el => {
            el.style.opacity = "1";
            el.style.transform = "none";
        });
    }

});
