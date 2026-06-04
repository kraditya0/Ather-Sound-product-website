document.addEventListener("DOMContentLoaded", () => {
    
    // --- 1. Category Filtering with GSAP Staggers ---
    const filterButtons = document.querySelectorAll(".gallery-filter-btn");
    const galleryItems = document.querySelectorAll(".gallery-item");

    if (filterButtons.length > 0 && galleryItems.length > 0) {
        filterButtons.forEach(btn => {
            btn.addEventListener("click", () => {
                // Toggle active styles on buttons
                filterButtons.forEach(b => {
                    b.classList.remove("text-brand-gold", "border-brand-gold");
                    b.classList.add("text-neutral-600", "dark:text-neutral-400");
                });
                btn.classList.add("text-brand-gold", "border-brand-gold");
                btn.classList.remove("text-neutral-600", "dark:text-neutral-400");

                const filter = btn.getAttribute("data-filter");

                if (typeof gsap !== "undefined") {
                    // Modern GSAP Grid Filter Animation
                    const toHide = [];
                    const toShow = [];

                    galleryItems.forEach(item => {
                        const itemCat = item.getAttribute("data-category");
                        if (filter === "all" || itemCat === filter) {
                            toShow.push(item);
                        } else {
                            toHide.push(item);
                        }
                    });

                    // Hide unwanted items first
                    if (toHide.length > 0) {
                        gsap.to(toHide, {
                            scale: 0.8,
                            opacity: 0,
                            duration: 0.4,
                            stagger: 0.05,
                            ease: "power2.inOut",
                            onComplete: () => {
                                toHide.forEach(el => el.classList.add("hidden"));
                            }
                        });
                    }

                    // Show selected items
                    toShow.forEach(el => el.classList.remove("hidden"));
                    gsap.fromTo(toShow, 
                        { scale: 0.8, opacity: 0 },
                        {
                            scale: 1,
                            opacity: 1,
                            duration: 0.5,
                            stagger: 0.05,
                            ease: "power2.out",
                            delay: toHide.length > 0 ? 0.25 : 0
                        }
                    );
                } else {
                    // Fallback filtering if GSAP fails
                    galleryItems.forEach(item => {
                        const itemCat = item.getAttribute("data-category");
                        if (filter === "all" || itemCat === filter) {
                            item.classList.remove("hidden");
                        } else {
                            item.classList.add("hidden");
                        }
                    });
                }
            });
        });
    }

    // --- 2. Lightbox Zoom / Pan Functionality ---
    const lightbox = document.getElementById("lightbox");
    const lightboxImg = document.getElementById("lightbox-image");
    const closeLightboxBtn = document.getElementById("close-lightbox");
    
    // Track click triggers
    galleryItems.forEach(item => {
        item.addEventListener("click", () => {
            const imageUrl = item.getAttribute("data-image-url");
            const videoUrl = item.getAttribute("data-video-url");

            if (imageUrl) {
                // Trigger Image Lightbox
                lightboxImg.src = imageUrl;
                lightbox.classList.add("opacity-100", "pointer-events-auto");
                document.body.style.overflow = "hidden"; // Prevent background scroll
                resetLightboxZoom();
            } else if (videoUrl) {
                // Trigger Video Modal Player
                openVideoModal(videoUrl);
            }
        });
    });

    if (lightbox) {
        // Close on background click or button click
        lightbox.addEventListener("click", (e) => {
            if (e.target === lightbox || e.target === closeLightboxBtn || closeLightboxBtn.contains(e.target)) {
                lightbox.classList.remove("opacity-100", "pointer-events-auto");
                document.body.style.overflow = "";
            }
        });
        
        // Escape key dismiss
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                lightbox.classList.remove("opacity-100", "pointer-events-auto");
                document.body.style.overflow = "";
            }
        });

        // Zoom coordinate / dragging parameters
        let isZoomed = false;
        let startX = 0, startY = 0, currentX = 0, currentY = 0;
        let dragStart = false;

        lightboxImg.addEventListener("dblclick", () => {
            if (!isZoomed) {
                lightboxImg.style.transform = "scale(2)";
                lightboxImg.classList.replace("cursor-grab", "cursor-move");
                isZoomed = true;
            } else {
                resetLightboxZoom();
            }
        });

        lightboxImg.addEventListener("mousedown", (e) => {
            if (!isZoomed) return;
            dragStart = true;
            startX = e.clientX - currentX;
            startY = e.clientY - currentY;
            lightboxImg.classList.replace("cursor-move", "cursor-grabbing");
        });

        document.addEventListener("mousemove", (e) => {
            if (!dragStart || !isZoomed) return;
            currentX = e.clientX - startX;
            currentY = e.clientY - startY;
            lightboxImg.style.transform = `scale(2) translate(${currentX / 2}px, ${currentY / 2}px)`;
        });

        document.addEventListener("mouseup", () => {
            if (dragStart) {
                dragStart = false;
                lightboxImg.classList.replace("cursor-grabbing", "cursor-move");
            }
        });

        function resetLightboxZoom() {
            lightboxImg.style.transform = "scale(1) translate(0px, 0px)";
            lightboxImg.classList.add("cursor-grab");
            lightboxImg.classList.remove("cursor-move", "cursor-grabbing");
            isZoomed = false;
            currentX = 0;
            currentY = 0;
        }
    }

    // --- 3. Video Modal Player ---
    const videoModal = document.getElementById("video-modal");
    const modalVideoPlayer = document.getElementById("modal-video-player");
    const closeVideoModalBtn = document.getElementById("close-video-modal");

    function openVideoModal(url) {
        if (!videoModal || !modalVideoPlayer) return;
        modalVideoPlayer.src = url;
        videoModal.classList.add("opacity-100", "pointer-events-auto");
        modalVideoPlayer.play().catch(err => console.log("Auto playback issue in modal: ", err));
        document.body.style.overflow = "hidden";
    }

    if (videoModal) {
        videoModal.addEventListener("click", (e) => {
            if (e.target === videoModal || e.target === closeVideoModalBtn || closeVideoModalBtn.contains(e.target)) {
                closeVideoModal();
            }
        });
        
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                closeVideoModal();
            }
        });
    }

    function closeVideoModal() {
        if (!videoModal || !modalVideoPlayer) return;
        modalVideoPlayer.pause();
        modalVideoPlayer.src = "";
        videoModal.classList.remove("opacity-100", "pointer-events-auto");
        document.body.style.overflow = "";
    }

});
