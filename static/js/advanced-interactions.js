// Advanced UI Interactions - Next Level

// Spotlight Effect that follows cursor
function initSpotlightEffect() {
    const cards = document.querySelectorAll('.card-spotlight, .article-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });
}

// Magnetic Button Effect
function initMagneticButtons() {
    const buttons = document.querySelectorAll('.btn-magnetic, .chip-modern');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transition = 'transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)';
        });
        
        button.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            
            const moveX = x * 0.15;
            const moveY = y * 0.15;
            
            this.style.transform = `translate(${moveX}px, ${moveY}px) scale(1.05)`;
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translate(0, 0) scale(1)';
        });
    });
}

// Enhanced Card 3D Tilt
function init3DTilt() {
    const cards = document.querySelectorAll('.article-card, .glass');
    
    cards.forEach(card => {
        let rafId = null;

        card.addEventListener('mousemove', (e) => {
            if (rafId) return;
            rafId = requestAnimationFrame(() => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = ((y - centerY) / centerY) * 5;
                const rotateY = ((centerX - x) / centerX) * 5;
                
                card.style.transform = `
                    perspective(1000px) 
                    rotateX(${-rotateX}deg) 
                    rotateY(${rotateY}deg) 
                    translateZ(10px)
                    scale3d(1.02, 1.02, 1.02)
                `;
                rafId = null;
            });
        });
        
        card.addEventListener('mouseleave', () => {
            if (rafId) {
                cancelAnimationFrame(rafId);
                rafId = null;
            }
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateZ(0) scale3d(1, 1, 1)';
        });
    });
}

// Parallax Scrolling for Background Elements
function initParallaxScroll() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    if (!parallaxElements.length) return;
    
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                parallaxElements.forEach(element => {
                    const speed = parseFloat(element.dataset.parallax) || 0.5;
                    const yPos = -(scrolled * speed);
                    element.style.transform = `translate3d(0, ${yPos}px, 0)`;
                });
                ticking = false;
            });
            ticking = true;
        }
    }, { passive: true });
}

// Smooth Scroll with Easing
function smoothScrollTo(target, duration = 1000) {
    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;
    
    function easeInOutCubic(t) {
        return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
    }
    
    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        const ease = easeInOutCubic(progress);
        
        window.scrollTo(0, startPosition + distance * ease);
        
        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }
    
    requestAnimationFrame(animation);
}

// Enhanced Toast with Animations
function showAdvancedToast(message, type = 'success', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-[9999] glass-pro rounded-2xl p-4 shadow-2xl transform translate-x-full transition-all duration-500 border-glow`;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    const colors = {
        success: 'border-l-4 border-green-500',
        error: 'border-l-4 border-red-500',
        warning: 'border-l-4 border-yellow-500',
        info: 'border-l-4 border-blue-500'
    };
    
    toast.classList.add(colors[type]);
    toast.innerHTML = `
        <div class="flex items-center space-x-3 min-w-[300px]">
            <span class="text-3xl animate-bounce">${icons[type]}</span>
            <span class="text-sm font-medium flex-1">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="text-gray-400 hover:text-gray-200 transition-colors">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
                </svg>
            </button>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Slide in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 10);
    
    // Auto dismiss
    setTimeout(() => {
        toast.style.transform = 'translateX(150%)';
        setTimeout(() => toast.remove(), 500);
    }, duration);
}

// Intersection Observer for Scroll Animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('revealed');
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100); // Stagger effect
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.scroll-reveal, .stagger-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        observer.observe(el);
    });
}

// Loading State Manager
class LoadingManager {
    static show(element) {
        element.classList.add('loading-pulse');
        element.style.pointerEvents = 'none';
        element.style.opacity = '0.6';
    }
    
    static hide(element) {
        element.classList.remove('loading-pulse');
        element.style.pointerEvents = '';
        element.style.opacity = '1';
    }
    
    static showSkeleton(container, count = 3) {
        const skeleton = `
            <div class="space-y-4">
                ${Array(count).fill('').map(() => `
                    <div class="glass rounded-2xl p-6 space-y-3">
                        <div class="skeleton-advanced h-48 rounded-xl"></div>
                        <div class="skeleton-advanced h-4 rounded"></div>
                        <div class="skeleton-advanced h-4 rounded w-3/4"></div>
                        <div class="flex gap-2">
                            <div class="skeleton-advanced h-6 w-20 rounded-full"></div>
                            <div class="skeleton-advanced h-6 w-20 rounded-full"></div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.innerHTML = skeleton;
    }
}

// Enhanced Search with Debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Keyboard Shortcuts Manager
class KeyboardShortcuts {
    constructor() {
        this.shortcuts = new Map();
        this.init();
    }
    
    init() {
        document.addEventListener('keydown', (e) => {
            const key = e.key.toLowerCase();
            const ctrl = e.ctrlKey || e.metaKey;
            const shortcutKey = `${ctrl ? 'ctrl+' : ''}${key}`;
            
            if (this.shortcuts.has(shortcutKey)) {
                e.preventDefault();
                this.shortcuts.get(shortcutKey)();
            }
        });
    }
    
    register(key, callback) {
        this.shortcuts.set(key, callback);
    }
}

// Initialize keyboard shortcuts
const shortcuts = new KeyboardShortcuts();
shortcuts.register('/', () => {
    const searchInput = document.getElementById('searchInput');
    if (searchInput && document.activeElement !== searchInput) {
        searchInput.focus();
        searchInput.select();
    }
});

shortcuts.register('escape', () => {
    document.activeElement.blur();
});

// Floating Action Menu
function initFloatingActionMenu() {
    const fabButton = document.getElementById('scrollToTop');
    if (!fabButton) return;
    
    let lastScrollTop = 0;
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 300) {
            fabButton.style.opacity = '1';
            fabButton.style.visibility = 'visible';
            
            if (scrollTop > lastScrollTop) {
                // Scrolling down
                fabButton.style.transform = 'scale(0.8)';
            } else {
                // Scrolling up
                fabButton.style.transform = 'scale(1)';
            }
        } else {
            fabButton.style.opacity = '0';
            fabButton.style.visibility = 'hidden';
        }
        
        lastScrollTop = scrollTop;
    }, { passive: true });
}

// Image Lazy Load with Blur Effect
function initImageLazyLoad() {
    const images = document.querySelectorAll('img[loading="lazy"]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.style.filter = 'blur(20px)';
                img.style.transition = 'filter 0.8s cubic-bezier(0.4, 0, 0.2, 1)';
                
                if (img.complete) {
                    img.style.filter = 'blur(0)';
                } else {
                    img.addEventListener('load', () => {
                        img.style.filter = 'blur(0)';
                    }, { once: true });
                }
                
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Copy to Clipboard with Visual Feedback
async function copyToClipboardAdvanced(text, button) {
    try {
        await navigator.clipboard.writeText(text);
        
        // Visual feedback
        const original = button.innerHTML;
        button.innerHTML = '✓ Copied!';
        button.classList.add('elastic');
        
        showAdvancedToast('Copied to clipboard!', 'success', 2000);
        
        setTimeout(() => {
            button.innerHTML = original;
            button.classList.remove('elastic');
        }, 2000);
    } catch (err) {
        showAdvancedToast('Failed to copy', 'error');
    }
}

// Performance Monitoring
class PerformanceMonitor {
    constructor() {
        this.marks = new Map();
    }
    
    start(label) {
        this.marks.set(label, performance.now());
    }
    
    end(label) {
        const start = this.marks.get(label);
        if (start) {
            const duration = performance.now() - start;
            console.log(`⏱️ ${label}: ${duration.toFixed(2)}ms`);
            this.marks.delete(label);
            return duration;
        }
    }
}

// Initialize all advanced features
document.addEventListener('DOMContentLoaded', () => {
    const perfMonitor = new PerformanceMonitor();
    perfMonitor.start('initialization');
    
    // Initialize all features
    initSpotlightEffect();
    initMagneticButtons();
    init3DTilt();
    initParallaxScroll();
    initScrollAnimations();
    initFloatingActionMenu();
    initImageLazyLoad();
    
    perfMonitor.end('initialization');
    
    console.log('🚀 Advanced UI initialized successfully!');
});

// Export utilities
window.AdvancedUI = {
    showToast: showAdvancedToast,
    LoadingManager,
    PerformanceMonitor,
    copyToClipboard: copyToClipboardAdvanced,
    smoothScrollTo,
    debounce
};
