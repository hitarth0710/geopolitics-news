// Modern UI Enhancements and Interactions

// Smooth Scroll Reveal Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const revealOnScroll = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Apply scroll reveal to stagger items
document.addEventListener('DOMContentLoaded', () => {
    const staggerItems = document.querySelectorAll('.stagger-item');
    staggerItems.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(30px)';
        revealOnScroll.observe(item);
    });
});

// Scroll Progress Bar
function updateScrollProgress() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    
    let progressBar = document.getElementById('scrollProgress');
    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.id = 'scrollProgress';
        progressBar.className = 'progress-bar';
        document.body.appendChild(progressBar);
    }
    progressBar.style.width = scrolled + '%';
}

window.addEventListener('scroll', updateScrollProgress);

// Ripple Effect for Buttons
function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    
    ripple.style.width = ripple.style.height = `${diameter}px`;
    ripple.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    ripple.style.top = `${event.clientY - button.offsetTop - radius}px`;
    ripple.classList.add('ripple-effect');
    
    const rippleEffect = button.getElementsByClassName('ripple-effect')[0];
    if (rippleEffect) {
        rippleEffect.remove();
    }
    
    button.appendChild(ripple);
}

// Apply ripple to all buttons
document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('button, .btn-modern');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
});

// Toast Notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="flex items-center space-x-3">
            <span class="text-2xl">${type === 'success' ? '✅' : '❌'}</span>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Smooth Scroll to Top
function smoothScrollToTop() {
    const scrollDuration = 600;
    const scrollStep = -window.scrollY / (scrollDuration / 15);
    const scrollInterval = setInterval(() => {
        if (window.scrollY !== 0) {
            window.scrollBy(0, scrollStep);
        } else {
            clearInterval(scrollInterval);
        }
    }, 15);
}

// Enhanced Card Hover Effect with 3D Tilt
function initCard3D() {
    const cards = document.querySelectorAll('.article-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initCard3D);

// Lazy Load Images with Blur Effect
function lazyLoadImages() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.style.filter = 'blur(10px)';
                img.style.transition = 'filter 0.5s';
                
                img.addEventListener('load', () => {
                    img.style.filter = 'blur(0)';
                });
                
                observer.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Parallax Effect for Background Elements
function initParallax() {
    const parallaxElements = document.querySelectorAll('.parallax');
    
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        
        parallaxElements.forEach(element => {
            const speed = element.dataset.speed || 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

document.addEventListener('DOMContentLoaded', initParallax);

// Cursor Trail Effect (Optional - can be disabled)
let cursorTrail = [];
const trailLength = 10;

function createCursorTrail() {
    document.addEventListener('mousemove', (e) => {
        const trail = document.createElement('div');
        trail.className = 'cursor-trail';
        trail.style.left = e.clientX + 'px';
        trail.style.top = e.clientY + 'px';
        
        document.body.appendChild(trail);
        cursorTrail.push(trail);
        
        setTimeout(() => {
            trail.style.opacity = '0';
            setTimeout(() => trail.remove(), 500);
        }, 100);
        
        if (cursorTrail.length > trailLength) {
            cursorTrail.shift();
        }
    });
}

// Uncomment to enable cursor trail
// document.addEventListener('DOMContentLoaded', createCursorTrail);

// Skeleton Loader for Content
function showSkeletonLoader(container) {
    const skeleton = `
        <div class="animate-pulse space-y-4">
            <div class="h-48 bg-gray-300 dark:bg-gray-700 rounded-xl skeleton"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded skeleton"></div>
            <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-5/6 skeleton"></div>
        </div>
    `;
    container.innerHTML = skeleton;
}

// Copy to Clipboard with Toast
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

// Dark Mode Toggle with Smooth Transition
function initDarkModeToggle() {
    const toggleButton = document.querySelector('[onclick*="toggleTheme"]');
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            document.documentElement.style.transition = 'background-color 0.3s, color 0.3s';
            setTimeout(() => {
                document.documentElement.style.transition = '';
            }, 300);
        });
    }
}

document.addEventListener('DOMContentLoaded', initDarkModeToggle);

// Form Validation with Modern Feedback
function enhanceFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required], textarea[required]');
        
        inputs.forEach(input => {
            input.addEventListener('invalid', (e) => {
                e.preventDefault();
                input.classList.add('border-red-500', 'shake');
                
                setTimeout(() => {
                    input.classList.remove('shake');
                }, 500);
            });
            
            input.addEventListener('input', () => {
                if (input.validity.valid) {
                    input.classList.remove('border-red-500');
                    input.classList.add('border-green-500');
                }
            });
        });
    });
}

document.addEventListener('DOMContentLoaded', enhanceFormValidation);

// Add shake animation to CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    .shake {
        animation: shake 0.5s;
    }
    .ripple-effect {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        pointer-events: none;
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
    }
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.ModernUI = {
    showToast,
    copyToClipboard,
    showSkeletonLoader,
    smoothScrollToTop
};
