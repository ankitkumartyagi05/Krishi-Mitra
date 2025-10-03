// Authentication Module

// DOM Elements
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');

// Initialize Authentication
function initializeAuth() {
    // Check if user is already logged in
    checkAuthStatus();
    
    // Form submission handlers
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
}

// Check Authentication Status
function checkAuthStatus() {
    const token = localStorage.getItem('authToken');
    if (token) {
        // Verify token with backend
        fetch('/auth/verify', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
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
        });
    }
}

// Handle Login
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
            updateUIForLoggedInUser(data.user);
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

// Handle Registration
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

// Update UI for Logged In User
function updateUIForLoggedInUser(userData) {
    // Update user info in chat
    document.getElementById('chat-username').textContent = userData.username;
    document.getElementById('chat-location').textContent = userData.location;
    
    // Hide login/register buttons
    document.getElementById('login-btn').style.display = 'none';
    document.getElementById('register-btn').style.display = 'none';
    
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
    window.location.reload();
}

// Add user menu styles
const userMenuStyles = document.createElement('style');
userMenuStyles.textContent = `
    .user-menu {
        position: relative;
        margin-left: 15px;
    }
    
    .user-avatar-small {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--primary-light);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        cursor: pointer;
    }
    
    .user-dropdown {
        position: absolute;
        top: 100%;
        right: 0;
        background-color: white;
        border-radius: 8px;
        box-shadow: var(--shadow);
        min-width: 150px;
        display: none;
        z-index: 1001;
    }
    
    .user-menu:hover .user-dropdown {
        display: block;
    }
    
    .user-dropdown a {
        display: block;
        padding: 10px 15px;
        color: var(--text-color);
        text-decoration: none;
        transition: background-color 0.3s ease;
    }
    
    .user-dropdown a:hover {
        background-color: var(--background-color);
    }
`;
document.head.appendChild(userMenuStyles);