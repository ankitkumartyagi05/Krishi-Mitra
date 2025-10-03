// Authentication Module

// DOM Elements
const loginBtn = document.getElementById('login-btn');
const registerBtn = document.getElementById('register-btn');
const authModal = document.getElementById('auth-modal');
const closeModal = document.querySelector('.close-btn');
const authTabs = document.querySelectorAll('.auth-tab');
const authForms = document.querySelectorAll('.auth-form');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const forgotPasswordLink = document.querySelector('.forgot-password');
const termsLink = document.querySelector('.terms-link');

// Initialize Authentication
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is already logged in
    checkAuthStatus();
    
    // Event listeners
    loginBtn.addEventListener('click', () => openAuthModal('login'));
    registerBtn.addEventListener('click', () => openAuthModal('register'));
    closeModal.addEventListener('click', closeAuthModal);
    authTabs.forEach(tab => tab.addEventListener('click', switchAuthTab));
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    forgotPasswordLink.addEventListener('click', handleForgotPassword);
    termsLink.addEventListener('click', handleTermsLink);
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === authModal) {
            closeAuthModal();
        }
    });
    
    // Password validation
    document.getElementById('register-password').addEventListener('input', validatePassword);
    document.getElementById('register-confirm-password').addEventListener('input', validatePasswordMatch);
});

// Check Authentication Status
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    if (token) {
        // Verify token with backend
        fetch('/auth/verify', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.valid) {
                updateUIForLoggedInUser(data.user);
            } else {
                // Token is invalid, remove it
                localStorage.removeItem('authToken');
                localStorage.removeItem('userData');
            }
        })
        .catch(error => {
            console.error('Auth verification error:', error);
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
        });
    }
}

// Open Auth Modal
function openAuthModal(tab) {
    authModal.style.display = 'block';
    switchAuthTab({ target: document.querySelector(`[data-tab="${tab}"]`) });
    
    // Clear any previous form data
    if (tab === 'login') {
        loginForm.reset();
    } else {
        registerForm.reset();
    }
    
    // Clear any previous error messages
    clearFormErrors();
}

// Close Auth Modal
function closeAuthModal() {
    authModal.style.display = 'none';
    clearFormErrors();
}

// Switch Auth Tab
function switchAuthTab(e) {
    const tabName = e.target.dataset.tab;
    
    // Update tab appearance
    authTabs.forEach(tab => tab.classList.remove('active'));
    e.target.classList.add('active');
    
    // Show corresponding form
    authForms.forEach(form => form.classList.remove('active'));
    document.getElementById(`${tabName}-form`).classList.add('active');
}

// Handle Login
function handleLogin(e) {
    e.preventDefault();
    
    // Clear previous errors
    clearFormErrors();
    
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const rememberMe = document.getElementById('remember-me').checked;
    
    // Validate form
    if (!validateLoginForm(email, password)) {
        return;
    }
    
    // Show loading state
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Logging in...';
    submitBtn.disabled = true;
    
    // Send login request to backend
    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Login failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Store auth token
            localStorage.setItem('authToken', data.token);
            localStorage.setItem('userData', JSON.stringify(data.user));
            
            // Remember me functionality
            if (rememberMe) {
                localStorage.setItem('rememberMe', 'true');
            } else {
                sessionStorage.setItem('authToken', data.token);
                sessionStorage.setItem('userData', JSON.stringify(data.user));
            }
            
            // Update UI
            updateUIForLoggedInUser(data.user);
            closeAuthModal();
            showNotification('Login successful! Welcome back.', 'success');
            
            // Redirect to dashboard if needed
            // window.location.href = '/dashboard';
        } else {
            showFormError('login', data.message || 'Invalid email or password');
        }
    })
    .catch(error => {
        console.error('Login error:', error);
        showFormError('login', 'An error occurred during login. Please try again.');
    })
    .finally(() => {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

// Handle Registration
function handleRegister(e) {
    e.preventDefault();
    
    // Clear previous errors
    clearFormErrors();
    
    const userData = {
        username: document.getElementById('register-username').value.trim(),
        email: document.getElementById('register-email').value.trim(),
        password: document.getElementById('register-password').value,
        location: document.getElementById('register-location').value.trim(),
        language: document.getElementById('register-language').value,
        farmSize: parseFloat(document.getElementById('register-farm-size').value) || null
    };
    
    // Validate form
    if (!validateRegisterForm(userData)) {
        return;
    }
    
    // Show loading state
    const submitBtn = registerForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Creating Account...';
    submitBtn.disabled = true;
    
    // Send registration request to backend
    fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Registration failed');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showNotification('Registration successful! Please check your email to verify your account.', 'success');
            
            // Switch to login tab
            switchAuthTab({ target: document.querySelector('[data-tab="login"]') });
            
            // Pre-fill email in login form
            document.getElementById('login-email').value = userData.email;
        } else {
            showFormError('register', data.message || 'Registration failed. Please try again.');
        }
    })
    .catch(error => {
        console.error('Registration error:', error);
        showFormError('register', 'An error occurred during registration. Please try again.');
    })
    .finally(() => {
        // Reset button state
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    });
}

// Validate Login Form
function validateLoginForm(email, password) {
    if (!email) {
        showFormError('login', 'Please enter your email address');
        return false;
    }
    
    if (!isValidEmail(email)) {
        showFormError('login', 'Please enter a valid email address');
        return false;
    }
    
    if (!password) {
        showFormError('login', 'Please enter your password');
        return false;
    }
    
    return true;
}

// Validate Register Form
function validateRegisterForm(userData) {
    if (!userData.username) {
        showFormError('register', 'Please enter your full name');
        return false;
    }
    
    if (userData.username.length < 3) {
        showFormError('register', 'Name must be at least 3 characters long');
        return false;
    }
    
    if (!userData.email) {
        showFormError('register', 'Please enter your email address');
        return false;
    }
    
    if (!isValidEmail(userData.email)) {
        showFormError('register', 'Please enter a valid email address');
        return false;
    }
    
    if (!userData.password) {
        showFormError('register', 'Please enter a password');
        return false;
    }
    
    if (userData.password.length < 8) {
        showFormError('register', 'Password must be at least 8 characters long');
        return false;
    }
    
    if (!userData.location) {
        showFormError('register', 'Please enter your farm location');
        return false;
    }
    
    if (!userData.language) {
        showFormError('register', 'Please select your preferred language');
        return false;
    }
    
    if (!document.getElementById('agree-terms').checked) {
        showFormError('register', 'Please agree to the terms and conditions');
        return false;
    }
    
    return true;
}

// Validate Password Strength
function validatePassword() {
    const password = document.getElementById('register-password').value;
    const strengthIndicator = document.getElementById('password-strength');
    
    if (!strengthIndicator) return;
    
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]+/)) strength++;
    if (password.match(/[A-Z]+/)) strength++;
    if (password.match(/[0-9]+/)) strength++;
    if (password.match(/[$@#&!]+/)) strength++;
    
    // Update strength indicator
    strengthIndicator.className = 'password-strength';
    if (strength <= 2) {
        strengthIndicator.classList.add('weak');
        strengthIndicator.textContent = 'Weak';
    } else if (strength <= 3) {
        strengthIndicator.classList.add('medium');
        strengthIndicator.textContent = 'Medium';
    } else {
        strengthIndicator.classList.add('strong');
        strengthIndicator.textContent = 'Strong';
    }
}

// Validate Password Match
function validatePasswordMatch() {
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    const matchIndicator = document.getElementById('password-match');
    
    if (!matchIndicator) return;
    
    if (confirmPassword && password !== confirmPassword) {
        matchIndicator.textContent = 'Passwords do not match';
        matchIndicator.className = 'password-match error';
    } else if (confirmPassword && password === confirmPassword) {
        matchIndicator.textContent = 'Passwords match';
        matchIndicator.className = 'password-match success';
    } else {
        matchIndicator.textContent = '';
        matchIndicator.className = 'password-match';
    }
}

// Handle Forgot Password
function handleForgotPassword(e) {
    e.preventDefault();
    
    const email = prompt('Please enter your email address:');
    if (!email) return;
    
    if (!isValidEmail(email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    // Send password reset request
    fetch('/auth/forgot-password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('Password reset link sent to your email', 'success');
        } else {
            showNotification(data.message || 'Failed to send reset link', 'error');
        }
    })
    .catch(error => {
        console.error('Forgot password error:', error);
        showNotification('An error occurred. Please try again.', 'error');
    });
}

// Handle Terms Link
function handleTermsLink(e) {
    e.preventDefault();
    // Open terms and conditions in a new window or modal
    window.open('/terms', '_blank');
}

// Update UI for Logged In User
function updateUIForLoggedInUser(userData) {
    // Update user info in chat
    document.getElementById('chat-username').textContent = userData.username || userData.email;
    document.getElementById('chat-location').textContent = userData.location || 'Location not set';
    
    // Hide login/register buttons
    loginBtn.style.display = 'none';
    registerBtn.style.display = 'none';
    
    // Add user menu
    const userMenu = document.createElement('div');
    userMenu.className = 'user-menu';
    userMenu.innerHTML = `
        <div class="user-avatar-small">
            <i class="fas fa-user"></i>
        </div>
        <div class="user-dropdown">
            <a href="#profile">My Profile</a>
            <a href="#" id="logout-btn">Logout</a>
        </div>
    `;
    
    document.querySelector('.nav-controls').appendChild(userMenu);
    
    // Add logout functionality
    document.getElementById('logout-btn').addEventListener('click', logout);
}

// Logout
function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    sessionStorage.removeItem('authToken');
    sessionStorage.removeItem('userData');
    localStorage.removeItem('rememberMe');
    
    // Reload page to reset UI
    window.location.reload();
}

// Utility Functions
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFormError(form, message) {
    const formElement = document.getElementById(`${form}-form`);
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    
    // Remove any existing error
    const existingError = formElement.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add new error
    formElement.insertBefore(errorElement, formElement.firstChild);
}

function clearFormErrors() {
    const errors = document.querySelectorAll('.form-error');
    errors.forEach(error => error.remove());
}

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

// Add CSS for form elements
const authStyles = document.createElement('style');
authStyles.textContent = `
    .form-group {
        margin-bottom: 20px;
    }
    
    .form-group label {
        display: block;
        margin-bottom: 8px;
        font-weight: 500;
        color: #333;
    }
    
    .form-group input,
    .form-group select {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 4px;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .form-group input:focus,
    .form-group select:focus {
        outline: none;
        border-color: #2E7D32;
        box-shadow: 0 0 0 3px rgba(46, 125, 50, 0.1);
    }
    
    .checkbox-container {
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    
    .checkbox-container input[type="checkbox"] {
        display: none;
    }
    
    .checkmark {
        width: 20px;
        height: 20px;
        border: 2px solid #ddd;
        border-radius: 4px;
        margin-right: 10px;
        position: relative;
        transition: all 0.3s ease;
    }
    
    .checkbox-container input[type="checkbox"]:checked + .checkmark {
        background-color: #2E7D32;
        border-color: #2E7D32;
    }
    
    .checkbox-container input[type="checkbox"]:checked + .checkmark::after {
        content: '\\2713';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 14px;
    }
    
    .form-error {
        background-color: #ffebee;
        color: #c62828;
        padding: 10px 15px;
        border-radius: 4px;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }
    
    .form-footer {
        text-align: center;
        margin-top: 15px;
    }
    
    .form-footer a {
        color: #2E7D32;
        text-decoration: none;
        font-size: 0.9rem;
    }
    
    .form-footer a:hover {
        text-decoration: underline;
    }
    
    .password-strength {
        margin-top: 5px;
        font-size: 0.85rem;
    }
    
    .password-strength.weak {
        color: #f44336;
    }
    
    .password-strength.medium {
        color: #ff9800;
    }
    
    .password-strength.strong {
        color: #4caf50;
    }
    
    .password-match {
        margin-top: 5px;
        font-size: 0.85rem;
    }
    
    .password-match.error {
        color: #f44336;
    }
    
    .password-match.success {
        color: #4caf50;
    }
    
    .terms-link {
        color: #2E7D32;
        text-decoration: none;
    }
    
    .terms-link:hover {
        text-decoration: underline;
    }
`;
document.head.appendChild(authStyles);
