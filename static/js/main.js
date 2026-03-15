// Main JavaScript for Education Portal

document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    // Close alert messages after specific timeout
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Check if this is a welcome back message (admin login)
        const isWelcomeMessage = alert.textContent.includes('Welcome back');
        const timeout = isWelcomeMessage ? 3500 : 5000; // 3.5 seconds for welcome, 5 seconds for others
        
        setTimeout(() => {
            if (alert.style.display !== 'none') {
                alert.style.transition = 'opacity 0.3s ease';
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 300);
            }
        }, timeout);
    });
    
    // Add click handler to close alerts manually
    const closeButtons = document.querySelectorAll('.close-alert');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.transition = 'opacity 0.3s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        });
    });
}

function copyCode(code) {
    navigator.clipboard.writeText(code).then(() => {
        showNotification('Code copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Could not copy: ', err);
        showNotification('Failed to copy', 'error');
    });
}

function copyLink(link) {
    navigator.clipboard.writeText(link).then(() => {
        showNotification('Link copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Could not copy: ', err);
        showNotification('Failed to copy', 'error');
    });
}

function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        <span>${message}</span>
        <button class="alert-close" onclick="this.parentElement.style.display='none';">&times;</button>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.style.transition = 'opacity 0.3s ease';
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            alertDiv.remove();
        }, 300);
    }, 4000);
}

// Share functions for referral page
function shareOnWhatsApp() {
    const referralLink = document.getElementById('referralLink');
    if (referralLink) {
        const link = referralLink.value;
        const message = `Join me on EduPortal and get ₹100 bonus! ${link}`;
        const whatsappUrl = `https://wa.me/?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    }
}

function shareOnTwitter() {
    const referralLink = document.getElementById('referralLink');
    if (referralLink) {
        const link = referralLink.value;
        const message = `Join me on EduPortal! Learn amazing courses and earn rewards! ${link}`;
        const twitterUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(message)}`;
        window.open(twitterUrl, '_blank');
    }
}

function shareOnFacebook() {
    const referralLink = document.getElementById('referralLink');
    if (referralLink) {
        const link = referralLink.value;
        const facebookUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(link)}`;
        window.open(facebookUrl, '_blank');
    }
}

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

// Search functionality
function searchCourses(query) {
    const courseCards = document.querySelectorAll('.course-card');
    const lowerQuery = query.toLowerCase();
    
    courseCards.forEach(card => {
        const title = card.querySelector('.course-header h3')?.textContent.toLowerCase() || '';
        const description = card.querySelector('.course-body p')?.textContent.toLowerCase() || '';
        
        if (title.includes(lowerQuery) || description.includes(lowerQuery)) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// Filter courses by domain
function filterByDomain(domainId) {
    const courseCards = document.querySelectorAll('.course-card');
    
    courseCards.forEach(card => {
        if (domainId === 'all' || card.dataset.domain === domainId) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// Sort courses
function sortCourses(sortBy) {
    const container = document.querySelector('.courses-grid');
    const courses = Array.from(document.querySelectorAll('.course-card'));
    
    courses.sort((a, b) => {
        switch(sortBy) {
            case 'title':
                return a.querySelector('h3')?.textContent.localeCompare(b.querySelector('h3')?.textContent || '') || 0;
            case 'price':
                const priceA = parseFloat(a.querySelector('.price')?.textContent.replace('₹', '') || 0);
                const priceB = parseFloat(b.querySelector('.price')?.textContent.replace('₹', '') || 0);
                return priceA - priceB;
            default:
                return 0;
        }
    });
    
    container.innerHTML = '';
    courses.forEach(course => {
        container.appendChild(course);
    });
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Toggle dropdown menu
function toggleDropdown(element) {
    element.classList.toggle('active');
}

// Format currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Progress bar animation
function animateProgressBar(element, target) {
    const current = parseFloat(element.style.width) || 0;
    const increment = (target - current) / 10;
    let step = 0;
    
    const interval = setInterval(() => {
        step++;
        const newWidth = current + (increment * step);
        element.style.width = Math.min(newWidth, target) + '%';
        
        if (newWidth >= target) {
            clearInterval(interval);
        }
    }, 50);
}

// Export functions if needed
window.copyCode = copyCode;
window.copyLink = copyLink;
window.showNotification = showNotification;
window.shareOnWhatsApp = shareOnWhatsApp;
window.shareOnTwitter = shareOnTwitter;
window.shareOnFacebook = shareOnFacebook;
window.searchCourses = searchCourses;
window.filterByDomain = filterByDomain;
window.sortCourses = sortCourses;
window.scrollToSection = scrollToSection;
window.toggleDropdown = toggleDropdown;
window.formatCurrency = formatCurrency;
window.animateProgressBar = animateProgressBar;
