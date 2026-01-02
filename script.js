// Mobile Navigation Toggle
const hamburger = document.getElementById('hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger
        const spans = hamburger.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translateY(8px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translateY(-8px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const spans = hamburger.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    });
});

// Navbar scroll effect
const navbar = document.getElementById('navbar');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    
    lastScroll = currentScroll;
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            const navHeight = navbar.offsetHeight;
            
            // For project cards, calculate precise position
            if (target.classList && target.classList.contains('project-card')) {
                // Get computed scroll-margin-top value (default 120px from CSS)
                const computedStyle = window.getComputedStyle(target);
                const scrollMarginTop = parseInt(computedStyle.scrollMarginTop) || 120;
                
                // Calculate target position accounting for navbar and scroll margin
                const rect = target.getBoundingClientRect();
                const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
                const targetPosition = rect.top + scrollTop - navHeight - scrollMarginTop;
                
                window.scrollTo({
                    top: Math.max(0, targetPosition),
                    behavior: 'smooth'
                });
            } else {
                // For section links, use offset calculation
                const targetPosition = target.offsetTop - navHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        }
    });
});

// Active navigation link on scroll
const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.nav-link');

function updateActiveNavLink() {
    let current = '';
    const navHeight = navbar.offsetHeight;
    const scrollPosition = window.pageYOffset;
    
    // If we're at the very top, activate the first section (home)
    if (scrollPosition < 100) {
        current = sections[0] ? sections[0].getAttribute('id') : '';
    } else {
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (scrollPosition >= (sectionTop - navHeight - 100)) {
                current = section.getAttribute('id');
            }
        });
    }
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
}

// Update on scroll
window.addEventListener('scroll', updateActiveNavLink);

// Update on initial page load
updateActiveNavLink();

// Experience tabs functionality
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const targetTab = button.getAttribute('data-tab');
        
        // Remove active class from all buttons and contents
        tabButtons.forEach(btn => btn.classList.remove('active'));
        tabContents.forEach(content => content.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        document.getElementById(targetTab).classList.add('active');
    });
});

// Intersection Observer for fade-in animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
const animateElements = document.querySelectorAll('.project-card, .skill-category, .education-item');
animateElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// Form validation (if you add a contact form later)
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Scroll to top functionality (optional enhancement)
const scrollToTop = document.createElement('button');
scrollToTop.innerHTML = '↑';
scrollToTop.className = 'scroll-to-top';
scrollToTop.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: var(--bg-primary);
    border: none;
    cursor: pointer;
    font-size: 24px;
    display: none;
    z-index: 999;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(100, 255, 218, 0.3);
`;

scrollToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTop.style.display = 'block';
    } else {
        scrollToTop.style.display = 'none';
    }
});

document.body.appendChild(scrollToTop);

// Add hover effect to scroll to top button
scrollToTop.addEventListener('mouseenter', () => {
    scrollToTop.style.transform = 'translateY(-5px)';
    scrollToTop.style.boxShadow = '0 8px 20px rgba(100, 255, 218, 0.5)';
});

scrollToTop.addEventListener('mouseleave', () => {
    scrollToTop.style.transform = 'translateY(0)';
    scrollToTop.style.boxShadow = '0 5px 15px rgba(100, 255, 218, 0.3)';
});

// Copy email to clipboard functionality
const emailAddress = 'sara_parvaresh@yahoo.com';

function copyEmailToClipboard(e) {
    e.preventDefault();
    navigator.clipboard.writeText(emailAddress).then(() => {
        // Show feedback
        const originalText = e.target.textContent || e.target.closest('a').textContent;
        const originalHTML = e.target.innerHTML || e.target.closest('a').innerHTML;
        
        if (e.target.id === 'email-btn') {
            e.target.textContent = 'Email Copied!';
            setTimeout(() => {
                e.target.textContent = originalText;
            }, 2000);
        } else {
            // For the icon link, we can add a small tooltip or change cursor
            const link = e.target.closest('a');
            const originalTitle = link.getAttribute('title') || '';
            link.setAttribute('title', 'Email Copied!');
            setTimeout(() => {
                link.setAttribute('title', originalTitle || 'Copy Email');
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy email:', err);
        // Fallback: try the old method
        const textArea = document.createElement('textarea');
        textArea.value = emailAddress;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            alert('Email copied to clipboard: ' + emailAddress);
        } catch (err) {
            alert('Please copy manually: ' + emailAddress);
        }
        document.body.removeChild(textArea);
    });
}

// Add event listeners for email links
const emailBtn = document.getElementById('email-btn');
const emailLink = document.getElementById('email-link');

if (emailBtn) {
    emailBtn.addEventListener('click', copyEmailToClipboard);
}

if (emailLink) {
    emailLink.addEventListener('click', copyEmailToClipboard);
    emailLink.setAttribute('title', 'Click to copy email');
}

// Hero Carousel Functionality
const carouselTrack = document.querySelector('.carousel-track');
const carouselSlides = document.querySelectorAll('.carousel-slide');
const carouselDots = document.querySelectorAll('.carousel-dot');
const prevBtn = document.querySelector('.carousel-btn-prev');
const nextBtn = document.querySelector('.carousel-btn-next');
const carouselDescription = document.querySelector('.carousel-description');

let currentSlide = 0;
let autoSlideInterval;

// Initialize carousel if elements exist
if (carouselTrack && carouselSlides.length > 0) {
    // Function to show a specific slide
    function showSlide(index) {
        // Remove active class from all slides and dots
        carouselSlides.forEach(slide => slide.classList.remove('active'));
        carouselDots.forEach(dot => dot.classList.remove('active'));
        
        // Add active class to current slide and dot
        if (carouselSlides[index]) {
            carouselSlides[index].classList.add('active');
            
            // Update description if it exists
            if (carouselDescription) {
                const description = carouselSlides[index].getAttribute('data-description') || '';
                carouselDescription.style.opacity = '0';
                setTimeout(() => {
                    carouselDescription.textContent = description;
                    carouselDescription.style.opacity = '1';
                }, 150);
            }
        }
        if (carouselDots[index]) {
            carouselDots[index].classList.add('active');
        }
        
        currentSlide = index;
    }
    
    // Function to go to next slide
    function nextSlide() {
        const nextIndex = (currentSlide + 1) % carouselSlides.length;
        showSlide(nextIndex);
    }
    
    // Function to go to previous slide
    function prevSlide() {
        const prevIndex = (currentSlide - 1 + carouselSlides.length) % carouselSlides.length;
        showSlide(prevIndex);
    }
    
    // Auto-slide functionality (optional - can be removed if manual only)
    function startAutoSlide() {
        stopAutoSlide(); // Clear any existing timer first
        autoSlideInterval = setTimeout(() => {
            nextSlide(); // Advance to next slide
            startAutoSlide(); // Reset timer after automatic slide
        }, 8000); // Change slide every 8 seconds
    }
    
    function stopAutoSlide() {
        if (autoSlideInterval) {
            clearTimeout(autoSlideInterval);
            autoSlideInterval = null;
        }
    }
    
    // Event listeners for navigation buttons
    if (nextBtn) {
        nextBtn.addEventListener('click', () => {
            nextSlide();
            stopAutoSlide();
            startAutoSlide(); // Restart auto-slide after manual navigation
        });
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', () => {
            prevSlide();
            stopAutoSlide();
            startAutoSlide(); // Restart auto-slide after manual navigation
        });
    }
    
    // Event listeners for dots
    carouselDots.forEach((dot, index) => {
        dot.addEventListener('click', () => {
            showSlide(index);
            stopAutoSlide();
            startAutoSlide(); // Restart auto-slide after manual navigation
        });
    });
    
    // Pause auto-slide on hover
    const carouselContainer = document.querySelector('.carousel-container');
    if (carouselContainer) {
        carouselContainer.addEventListener('mouseenter', stopAutoSlide);
        carouselContainer.addEventListener('mouseleave', startAutoSlide);
    }
    
    // Start auto-slide (only if more than one slide)
    if (carouselSlides.length > 1) {
        startAutoSlide();
    }
    
    // Initialize first slide
    showSlide(0);
}
