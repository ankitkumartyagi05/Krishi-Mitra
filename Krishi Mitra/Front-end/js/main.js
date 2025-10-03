// DOM Elements
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');
const languageSelector = document.getElementById('language-selector');
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const authModal = document.getElementById('auth-modal');
const closeModal = document.querySelector('.close-btn');
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load user preferences
    loadUserPreferences();
    
    // Initialize sections
    initializeWeather();
    initializeMarket();
    initializeSoil();
    initializeChat();
    
    // Event listeners
    hamburger.addEventListener('click', toggleMobileMenu);
    navLinks.forEach(link => link.addEventListener('click', closeMobileMenu));
    languageSelector.addEventListener('change', changeLanguage);
    loginBtn.addEventListener('click', () => openAuthModal('login'));
    registerBtn.addEventListener('click', () => openAuthModal('register'));
    closeModal.addEventListener('click', closeAuthModal);
    authTabs.forEach(tab => tab.addEventListener('click', switchAuthTab));
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            closeAuthModal();
        }
    });
});

// Mobile Menu Toggle
function toggleMobileMenu() {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
}

function closeMobileMenu() {
    hamburger.classList.remove('active');
    navMenu.classList.remove('active');
}

// Language Change
function changeLanguage() {
    const selectedLanguage = languageSelector.value;
    localStorage.setItem('preferredLanguage', selectedLanguage);
    updateUILanguage(selectedLanguage);
    // Reload page to apply language changes
    window.location.reload();
}

function updateUILanguage(language) {
    // Update all text elements based on selected language
    document.documentElement.lang = language;
    // Additional language updates would be handled here
}

// Load User Preferences
function loadUserPreferences() {
    // Load language preference
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
        languageSelector.value = savedLanguage;
    }
    
    // Check if user is logged in
    const token = localStorage.getItem('authToken');
    if (token) {
        updateUIForLoggedInUser();
    }
}

// Authentication Modal
function openAuthModal(tab) {
    authModal.style.display = 'block';
    switchAuthTab({ target: document.querySelector(`[data-tab="${tab}"]`) });
}

function closeAuthModal() {
    authModal.style.display = 'none';
}

function switchAuthTab(e) {
    const tabName = e.target.dataset.tab;
    
    // Update tab appearance
    authTabs.forEach(tab => tab.classList.remove('active'));
    e.target.classList.add('active');
    
    // Show corresponding form
    authForms.forEach(form => form.classList.remove('active'));
    document.getElementById(`${tabName}-form`).classList.add('active');
}

// Authentication Handlers
function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    // Send login request to backend
    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userData', JSON.stringify(data.user));
            updateUIForLoggedInUser();
            closeAuthModal();
            showNotification('Login successful!', 'success');
        } else {
            showNotification(data.message || 'Login failed', 'error');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showNotification('An error occurred during login', 'error');
    });
}

function handleRegister(e) {
    e.preventDefault();
    
    const userData = {
        username: document.getElementById('register-username').value,
        email: document.getElementById('register-email').value,
        password: document.getElementById('register-password').value,
        location: document.getElementById('register-location').value,
        language: document.getElementById('register-language').value
    };
    
    // Send registration request to backend
    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Registration successful! Please login.', 'success');
            switchAuthTab({ target: document.querySelector('[data-tab="login"]') });
        } else {
            showNotification(data.message || 'Registration failed', 'error');
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        showNotification('An error occurred during registration', 'error');
    });
}

function updateUIForLoggedInUser() {
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    
    // Update UI elements
    if (userData.username) {
        document.getElementById('chat-username').textContent = userData.username;
    }
    
    if (userData.location) {
        document.getElementById('chat-location').textContent = userData.location;
    }
    
    // Hide login/register buttons and show user menu
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    
    // Add logout button
    const logoutBtn = document.createElement('button');
    logoutBtn.className = 'btn btn-outline';
    logoutBtn.textContent = 'Logout';
    logoutBtn.addEventListener('click', logout);
    document.querySelector('.nav-controls').appendChild(logoutBtn);
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    window.location.reload();
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Section Initializers
function initializeWeather() {
    // Weather initialization will be handled in weather.js
}

function initializeMarket() {
    // Market initialization will be handled in market.js
}

function initializeSoil() {
    // Soil initialization will be handled in soil.js
}

function initializeChat() {
    // Chat initialization will be handled in chat.js
}

// Utility Functions
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

function formatTime(dateString) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString(undefined, options);
}

function getWeatherIcon(weatherCode) {
    const icons = {
        '01d': 'fas fa-sun',
        '01n': 'fas fa-moon',
        '02d': 'fas fa-cloud-sun',
        '02n': 'fas fa-cloud-moon',
        '03d': 'fas fa-cloud',
        '03n': 'fas fa-cloud',
        '04d': 'fas fa-cloud',
        '04n': 'fas fa-cloud',
        '09d': 'fas fa-cloud-showers-heavy',
        '09n': 'fas fa-cloud-showers-heavy',
        '10d': 'fas fa-cloud-sun-rain',
        '10n': 'fas fa-cloud-moon-rain',
        '11d': 'fas fa-bolt',
        '11n': 'fas fa-bolt',
        '13d': 'fas fa-snowflake',
        '13n': 'fas fa-snowflake',
        '50d': 'fas fa-smog',
        '50n': 'fas fa-smog'
    };
    
    return icons[weatherCode] || 'fas fa-question';
}

// Add notification styles
const notificationStyles = document.createElement('style');
notificationStyles.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        border-radius: 4px;
        color: white;
        font-weight: 500;
        z-index: 3000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification-success {
        background-color: var(--success-color);
    }
    
    .notification-error {
        background-color: var(--error-color);
    }
    
    .notification-info {
        background-color: var(--info-color);
    }
    
    .notification-warning {
        background-color: var(--warning-color);
    }
`;
document.head.appendChild(notificationStyles);