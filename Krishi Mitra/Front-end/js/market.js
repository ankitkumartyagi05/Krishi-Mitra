// Market Module
let priceChart = null;
let currentCrop = null;
let currentState = null;

// DOM Elements
const cropSelector = document.getElementById('crop-selector');
const stateSelector = document.getElementById('state-selector');
const refreshPricesBtn = document.getElementById('refresh-prices');
const priceTableBody = document.getElementById('price-table-body');
const priceChartCanvas = document.getElementById('price-chart');

// Initialize Market Module
function initializeMarket() {
    // Event listeners
    cropSelector.addEventListener('change', handleCropChange);
    stateSelector.addEventListener('change', handleStateChange);
    refreshPricesBtn.addEventListener('click', refreshMarketData);
    
    // Initialize chart
    initializePriceChart();
    
    // Load initial data
    refreshMarketData();
}

// Handle Crop Change
function handleCropChange() {
    currentCrop = cropSelector.value;
    refreshMarketData();
}

// Handle State Change
function handleStateChange() {
    currentState = stateSelector.value;
    refreshMarketData();
}

// Refresh Market Data
function refreshMarketData() {
    const crop = cropSelector.value || 'wheat';
    const state = stateSelector.value || 'punjab';
    
    // Fetch current prices
    fetchMarketPrices(crop, state);
    
    // Fetch price history for chart
    fetchPriceHistory(crop, state);
    
    // Fetch price predictions
    fetchPricePredictions(crop, state);
}

// Fetch Market Prices
function fetchMarketPrices(crop, state) {
    // In a real implementation, you would fetch from your backend API
    // For demo purposes, we'll simulate data
    const mockData = [
        { market: 'Amritsar Mandi', district: 'Amritsar', price: 2100, change: 50 },
        { market: 'Jalandhar Mandi', district: 'Jalandhar', price: 2050, change: -30 },
        { market: 'Ludhiana Mandi', district: 'Ludhiana', price: 2150, change: 20 },
        { market: 'Patiala Mandi', district: 'Patiala', price: 2080, change: -10 },
        { market: 'Bathinda Mandi', district: 'Bathinda', price: 2120, change: 40 }
    ];
    
    displayMarketPrices(mockData);
}

// Display Market Prices
function displayMarketPrices(prices) {
    priceTableBody.innerHTML = '';
    
    prices.forEach(price => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${price.market}</td>
            <td>${price.district}</td>
            <td>₹${price.price}</td>
            <td class="price-change ${price.change >= 0 ? 'price-up' : 'price-down'}">
                ${price.change >= 0 ? '+' : ''}₹${price.change}
            </td>
        `;
        
        priceTableBody.appendChild(row);
    });
}

// Initialize Price Chart
function initializePriceChart() {
    const ctx = priceChartCanvas.getContext('2d');
    
    priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Market Price (₹/Quintal)',
                data: [],
                borderColor: '#2E7D32',
                backgroundColor: 'rgba(46, 125, 50, 0.1)',
                borderWidth: 2,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: {
                        display: true,
                        text: 'Price (₹/Quintal)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Date'
                    }
                }
            }
        }
    });
}

// Fetch Price History
function fetchPriceHistory(crop, state) {
    // In a real implementation, you would fetch from your backend API
    // For demo purposes, we'll simulate data
    const labels = [];
    const data = [];
    const today = new Date();
    
    // Generate 30 days of data
    for (let i = 29; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        // Generate random price with trend
        const basePrice = 2000;
        const trend = (30 - i) * 5; // Upward trend
        const randomVariation = Math.random() * 200 - 100; // Random variation
        data.push(Math.round(basePrice + trend + randomVariation));
    }
    
    updatePriceChart(labels, data);
}

// Update Price Chart
function updatePriceChart(labels, data) {
    priceChart.data.labels = labels;
    priceChart.data.datasets[0].data = data;
    priceChart.update();
}

// Fetch Price Predictions
function fetchPricePredictions(crop, state) {
    // In a real implementation, you would fetch from your backend API
    // For demo purposes, we'll simulate data
    const predictions = {
        '1m': { price: 2250, confidence: 85 },
        '3m': { price: 2400, confidence: 75 },
        '6m': { price: 2600, confidence: 65 }
    };
    
    displayPricePredictions(predictions);
}

// Display Price Predictions
function displayPricePredictions(predictions) {
    document.getElementById('prediction-1m').textContent = predictions['1m'].price;
    document.getElementById('confidence-1m').textContent = predictions['1m'].confidence;
    
    document.getElementById('prediction-3m').textContent = predictions['3m'].price;
    document.getElementById('confidence-3m').textContent = predictions['3m'].confidence;
    
    document.getElementById('prediction-6m').textContent = predictions['6m'].price;
    document.getElementById('confidence-6m').textContent = predictions['6m'].confidence;
}