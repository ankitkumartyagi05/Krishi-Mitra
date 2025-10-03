// Weather Module
let weatherChart = null;
let currentLocation = null;

// DOM Elements
const locationElement = document.getElementById('current-location');
const tempElement = document.getElementById('current-temp');
const descElement = document.getElementById('weather-desc');
const humidityElement = document.getElementById('humidity');
const windElement = document.getElementById('wind-speed');
const precipitationElement = document.getElementById('precipitation');
const forecastGrid = document.getElementById('forecast-grid');
const alertsContainer = document.getElementById('weather-alerts');

// Initialize Weather Module
function initializeWeather() {
    // Get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => {
                const { latitude, longitude } = position.coords;
                currentLocation = { latitude, longitude };
                fetchWeatherData(latitude, longitude);
                fetchWeatherAlerts(latitude, longitude);
            },
            error => {
                console.error('Geolocation error:', error);
                showNotification('Unable to get your location. Using default location.', 'warning');
                // Use default location (e.g., New Delhi)
                fetchWeatherData(28.6139, 77.2090);
                fetchWeatherAlerts(28.6139, 77.2090);
            }
        );
    } else {
        showNotification('Geolocation is not supported by this browser.', 'error');
        // Use default location
        fetchWeatherData(28.6139, 77.2090);
        fetchWeatherAlerts(28.6139, 77.2090);
    }
    
    // Set up refresh button
    const refreshBtn = document.createElement('button');
    refreshBtn.className = 'btn btn-outline';
    refreshBtn.innerHTML = '<i class="fas fa-sync-alt"></i> Refresh';
    refreshBtn.addEventListener('click', () => {
        if (currentLocation) {
            fetchWeatherData(currentLocation.latitude, currentLocation.longitude);
            fetchWeatherAlerts(currentLocation.latitude, currentLocation.longitude);
        }
    });
    
    const weatherSection = document.querySelector('.weather-section .container');
    weatherSection.insertBefore(refreshBtn, weatherSection.firstChild);
}

// Fetch Weather Data
function fetchWeatherData(lat, lon) {
    const apiKey = 'YOUR_OPENWEATHER_API_KEY'; // Replace with your API key
    const apiUrl = `https://api.openweathermap.org/data/2.5/onecall?lat=${lat}&lon=${lon}&exclude=minutely,hourly&appid=${apiKey}&units=metric`;
    
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            displayCurrentWeather(data.current);
            displayForecast(data.daily);
        })
        .catch(error => {
            console.error('Weather fetch error:', error);
            showNotification('Failed to fetch weather data', 'error');
        });
}

// Display Current Weather
function displayCurrentWeather(current) {
    // Update location
    locationElement.textContent = 'Your Location';
    
    // Update temperature
    tempElement.textContent = `${Math.round(current.temp)}°C`;
    
    // Update description
    descElement.textContent = current.weather[0].description;
    
    // Update details
    humidityElement.textContent = `${current.humidity}%`;
    windElement.textContent = `${current.wind_speed} km/h`;
    precipitationElement.textContent = `${current.pop * 100}%`;
    
    // Update weather icon
    const weatherIcon = document.querySelector('.weather-icon i');
    weatherIcon.className = getWeatherIcon(current.weather[0].icon);
}

// Display Weather Forecast
function displayForecast(daily) {
    forecastGrid.innerHTML = '';
    
    // Get next 5 days
    const forecastDays = daily.slice(1, 6);
    
    forecastDays.forEach(day => {
        const date = new Date(day.dt * 1000);
        const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
        
        const forecastItem = document.createElement('div');
        forecastItem.className = 'forecast-item';
        forecastItem.innerHTML = `
            <div class="forecast-day">${dayName}</div>
            <div class="forecast-icon">
                <i class="${getWeatherIcon(day.weather[0].icon)}"></i>
            </div>
            <div class="forecast-temp">${Math.round(day.temp.max)}° / ${Math.round(day.temp.min)}°</div>
        `;
        
        forecastGrid.appendChild(forecastItem);
    });
}

// Fetch Weather Alerts
function fetchWeatherAlerts(lat, lon) {
    // In a real implementation, you would fetch alerts from a weather API
    // For demo purposes, we'll simulate some alerts
    const alerts = [
        {
            type: 'warning',
            title: 'Heavy Rain Expected',
            description: 'Heavy rainfall expected in the next 24 hours. Take necessary precautions for your crops.'
        },
        {
            type: 'info',
            title: 'Temperature Rise',
            description: 'Temperatures are expected to rise significantly next week. Ensure adequate irrigation.'
        }
    ];
    
    displayWeatherAlerts(alerts);
}

// Display Weather Alerts
function displayWeatherAlerts(alerts) {
    alertsContainer.innerHTML = '';
    
    if (alerts.length === 0) {
        alertsContainer.innerHTML = '<p>No weather alerts at this time.</p>';
        return;
    }
    
    alerts.forEach(alert => {
        const alertItem = document.createElement('div');
        alertItem.className = `alert-item alert-${alert.type}`;
        alertItem.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <div>
                <h4>${alert.title}</h4>
                <p>${alert.description}</p>
            </div>
        `;
        
        alertsContainer.appendChild(alertItem);
    });
}

// Get Weather Icon Class
function getWeatherIcon(iconCode) {
    const iconMap = {
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
    
    return iconMap[iconCode] || 'fas fa-question';
}