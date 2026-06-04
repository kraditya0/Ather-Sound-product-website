document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. Product Card Hover Video Loop (Catalog Page) ---
    const cards = document.querySelectorAll(".product-card");
    cards.forEach(card => {
        const videoOverlay = card.querySelector(".video-preview-overlay");
        const video = card.querySelector("video");
        const img = card.querySelector(".product-image");
        
        if (videoOverlay && video && img) {
            card.addEventListener("mouseenter", () => {
                video.currentTime = 0;
                const playPromise = video.play();
                if (playPromise !== undefined) {
                    playPromise.then(() => {
                        img.style.opacity = "0.2";
                    }).catch(err => {
                        // Silent catch (autoplay restrictions, or mouseleft early)
                    });
                }
            });
            
            card.addEventListener("mouseleave", () => {
                video.pause();
                img.style.opacity = "1";
            });
        }
    });

    // --- 2. Thumbnail Swapping (Product Details) ---
    const thumbnailBtns = document.querySelectorAll(".thumbnail-btn");
    const mainProductImg = document.getElementById("main-product-image");
    
    if (thumbnailBtns.length > 0 && mainProductImg) {
        thumbnailBtns.forEach(btn => {
            btn.addEventListener("click", () => {
                const targetUrl = btn.getAttribute("data-image-url");
                if (targetUrl) {
                    mainProductImg.src = targetUrl;
                    
                    // Mark button active
                    thumbnailBtns.forEach(b => {
                        b.classList.replace("border-brand-gold", "border-transparent");
                    });
                    btn.classList.replace("border-transparent", "border-brand-gold");
                }
            });
        });
    }

    // --- 3. Image Magnifier Zoom Logic (Product Details) ---
    const zoomContainer = document.getElementById("zoom-container");
    if (zoomContainer && mainProductImg) {
        zoomContainer.addEventListener("mousemove", (e) => {
            const rect = zoomContainer.getBoundingClientRect();
            // Calculate percentage position
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            
            mainProductImg.style.transformOrigin = `${x}% ${y}%`;
            mainProductImg.style.transform = "scale(1.8)";
        });
        
        zoomContainer.addEventListener("mouseleave", () => {
            mainProductImg.style.transform = "scale(1)";
            mainProductImg.style.transformOrigin = "center center";
        });
    }

    // --- 4. Specs Accordion Tabs (Product Details) ---
    const accordionHeaders = document.querySelectorAll(".accordion-header");
    accordionHeaders.forEach(header => {
        header.addEventListener("click", () => {
            const targetId = header.getAttribute("data-target");
            const content = document.getElementById(targetId);
            const icon = header.querySelector(".fa-chevron-down");
            
            if (content && icon) {
                const isOpen = content.style.maxHeight && content.style.maxHeight !== "0px";
                
                // Close other items
                accordionHeaders.forEach(h => {
                    const tid = h.getAttribute("data-target");
                    const c = document.getElementById(tid);
                    const i = h.querySelector(".fa-chevron-down");
                    if (c && i) {
                        c.style.maxHeight = "0px";
                        i.style.transform = "rotate(0deg)";
                    }
                });

                if (!isOpen) {
                    // Open current item
                    content.style.maxHeight = `${content.scrollHeight}px`;
                    icon.style.transform = "rotate(180deg)";
                } else {
                    content.style.maxHeight = "0px";
                    icon.style.transform = "rotate(0deg)";
                }
            }
        });
    });

    // --- 5. Concierge Inquiry Form Toggle (Product Details) ---
    const formTrigger = document.getElementById("concierge-inquiry-trigger");
    const formContainer = document.getElementById("inquiry-form-container");
    
    if (formTrigger && formContainer) {
        formTrigger.addEventListener("click", () => {
            const isHidden = formContainer.classList.contains("hidden");
            if (isHidden) {
                formContainer.classList.remove("hidden");
                // GSAP smooth slide open if available
                if (typeof gsap !== "undefined") {
                    gsap.fromTo(formContainer, 
                        { height: 0, opacity: 0 }, 
                        { height: "auto", opacity: 1, duration: 0.6, ease: "power3.out" }
                    );
                }
                formTrigger.innerText = "Close Inquiry Form";
            } else {
                if (typeof gsap !== "undefined") {
                    gsap.to(formContainer, {
                        height: 0,
                        opacity: 0,
                        duration: 0.5,
                        ease: "power3.inOut",
                        onComplete: () => formContainer.classList.add("hidden")
                    });
                } else {
                    formContainer.classList.add("hidden");
                }
                formTrigger.innerText = "Submit Direct Inquiry Form";
            }
        });
    }

    // --- 6. Lightbox binding for primary image click ---
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-image");
    
    if (zoomContainer && lightbox && lightboxImg) {
        zoomContainer.addEventListener("click", (e) => {
            // Avoid triggering lightbox on scroll / coordinates zoom
            if (e.detail === 1) { // single click
                const mainImgSrc = mainProductImg.src;
                lightboxImg.src = mainImgSrc;
                lightbox.classList.add("opacity-100", "pointer-events-auto");
                document.body.style.overflow = "hidden";
            }
        });
    }

    // --- 7. Detail page video popup modal --
    const openVideoBtn = document.getElementById("open-video-btn");
    const videoModal = document.getElementById("video-modal");
    const modalVideoPlayer = document.getElementById("modal-video-player");
    const closeVideoModalBtn = document.getElementById("close-video-modal");

    if (openVideoBtn && videoModal && modalVideoPlayer) {
        openVideoBtn.addEventListener("click", () => {
            const videoUrl = openVideoBtn.getAttribute("data-video-url");
            modalVideoPlayer.src = videoUrl;
            videoModal.classList.add("opacity-100", "pointer-events-auto");
            modalVideoPlayer.play().catch(e => console.log("Play failed: ", e));
            document.body.style.overflow = "hidden";
        });
    }

    if (videoModal && closeVideoModalBtn) {
        const closePlayer = () => {
            modalVideoPlayer.pause();
            modalVideoPlayer.src = "";
            videoModal.classList.remove("opacity-100", "pointer-events-auto");
            document.body.style.overflow = "";
        };
        closeVideoModalBtn.addEventListener("click", closePlayer);
        videoModal.addEventListener("click", (e) => {
            if (e.target === videoModal) closePlayer();
        });
    }

    // --- 8. Stagger reveal product catalog list elements ---
    const catalogCards = document.querySelectorAll(".product-card-wrapper");
    if (catalogCards.length > 0) {
        if (typeof gsap !== "undefined") {
            gsap.to(catalogCards, {
                opacity: 1,
                y: 0,
                duration: 0.8,
                stagger: 0.1,
                ease: "power2.out",
                delay: 0.1
            });
        } else {
            catalogCards.forEach(card => {
                card.style.opacity = "1";
                card.style.transform = "none";
            });
        }
    }

});
