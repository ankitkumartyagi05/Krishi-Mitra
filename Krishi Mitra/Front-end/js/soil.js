// Soil Health Module
let currentSoilData = null;

// DOM Elements
const testSoilBtn = document.getElementById('test-soil-btn');
const manualTestBtn = document.getElementById('manual-test-btn');
const uploadArea = document.getElementById('upload-area');
const soilFileInput = document.getElementById('soil-file-input');

// Initialize Soil Module
function initializeSoil() {
    // Event listeners
    testSoilBtn.addEventListener('click', () => {
        uploadArea.click();
    });
    
    manualTestBtn.addEventListener('click', showManualTestForm);
    
    uploadArea.addEventListener('click', () => {
        soilFileInput.click();
    });
    
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2E7D32';
        uploadArea.style.backgroundColor = 'rgba(46, 125, 50, 0.05)';
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.style.borderColor = '#E0E0E0';
        uploadArea.style.backgroundColor = 'transparent';
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.style.borderColor = '#E0E0E0';
        uploadArea.style.backgroundColor = 'transparent';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleSoilFileUpload(files[0]);
        }
    });
    
    soilFileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleSoilFileUpload(e.target.files[0]);
        }
    });
    
    // Load sample soil data
    loadSampleSoilData();
}

// Load Sample Soil Data
function loadSampleSoilData() {
    // In a real implementation, you would fetch from your backend API
    // For demo purposes, we'll use sample data
    const sampleData = {
        ph: 6.8,
        nitrogen: 45,
        phosphorus: 22,
        potassium: 180,
        organic_matter: 2.5,
        texture: 'Loamy'
    };
    
    displaySoilData(sampleData);
    generateSoilRecommendations(sampleData);
}

// Display Soil Data
function displaySoilData(data) {
    currentSoilData = data;
    
    // Update pH
    document.getElementById('ph-value').textContent = data.ph;
    updateParameterIndicator('ph', data.ph, 6.0, 7.0);
    
    // Update Nitrogen
    document.getElementById('nitrogen-value').textContent = `${data.nitrogen} kg/ha`;
    updateParameterIndicator('nitrogen', data.nitrogen, 40, 60);
    
    // Update Phosphorus
    document.getElementById('phosphorus-value').textContent = `${data.phosphorus} kg/ha`;
    updateParameterIndicator('phosphorus', data.phosphorus, 20, 30);
    
    // Update Potassium
    document.getElementById('potassium-value').textContent = `${data.potassium} kg/ha`;
    updateParameterIndicator('potassium', data.potassium, 150, 200);
}

// Update Parameter Indicator
function updateParameterIndicator(param, value, minOptimal, maxOptimal) {
    const indicator = document.getElementById(`${param}-indicator`);
    const status = document.getElementById(`${param}-status`);
    
    if (value < minOptimal) {
        indicator.style.backgroundColor = '#F44336'; // Red - Low
        status.textContent = 'Low';
        status.style.color = '#F44336';
    } else if (value > maxOptimal) {
        indicator.style.backgroundColor = '#FF9800'; // Orange - High
        status.textContent = 'High';
        status.style.color = '#FF9800';
    } else {
        indicator.style.backgroundColor = '#4CAF50'; // Green - Optimal
        status.textContent = 'Optimal';
        status.style.color = '#4CAF50';
    }
}

// Generate Soil Recommendations
function generateSoilRecommendations(soilData) {
    // Generate crop recommendations
    const cropRecommendations = generateCropRecommendations(soilData);
    displayCropRecommendations(cropRecommendations);
    
    // Generate fertilizer recommendations
    const fertilizerRecommendations = generateFertilizerRecommendations(soilData);
    displayFertilizerRecommendations(fertilizerRecommendations);
}

// Generate Crop Recommendations
function generateCropRecommendations(soilData) {
    // In a real implementation, this would use an AI model
    // For demo purposes, we'll use simple rules
    const recommendations = [];
    
    if (soilData.ph >= 6.0 && soilData.ph <= 7.0) {
        recommendations.push({
            name: 'Wheat',
            reason: 'Optimal pH level for wheat cultivation',
            suitability: 'High'
        });
        recommendations.push({
            name: 'Rice',
            reason: 'Suitable pH and good water retention',
            suitability: 'Medium'
        });
    }
    
    if (soilData.nitrogen >= 40) {
        recommendations.push({
            name: 'Maize',
            reason: 'Adequate nitrogen levels',
            suitability: 'High'
        });
    }
    
    if (soilData.phosphorus >= 20) {
        recommendations.push({
            name: 'Soybean',
            reason: 'Good phosphorus content',
            suitability: 'Medium'
        });
    }
    
    return recommendations;
}

// Display Crop Recommendations
function displayCropRecommendations(recommendations) {
    const container = document.getElementById('crop-recommendations');
    container.innerHTML = '';
    
    recommendations.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <i class="fas fa-seedling"></i>
            <div>
                <h4>${rec.name}</h4>
                <p>${rec.reason}</p>
                <span class="suitability-badge suitability-${rec.suitability.toLowerCase()}">${rec.suitability} Suitability</span>
            </div>
        `;
        container.appendChild(item);
    });
}

// Generate Fertilizer Recommendations
function generateFertilizerRecommendations(soilData) {
    // In a real implementation, this would use an AI model
    // For demo purposes, we'll use simple rules
    const recommendations = [];
    
    if (soilData.nitrogen < 40) {
        recommendations.push({
            name: 'Urea',
            amount: '50-60 kg/ha',
            reason: 'Low nitrogen levels'
        });
    }
    
    if (soilData.phosphorus < 20) {
        recommendations.push({
            name: 'DAP',
            amount: '25-30 kg/ha',
            reason: 'Low phosphorus levels'
        });
    }
    
    if (soilData.potassium < 150) {
        recommendations.push({
            name: 'MOP',
            amount: '20-25 kg/ha',
            reason: 'Low potassium levels'
        });
    }
    
    if (soilData.organic_matter < 2.0) {
        recommendations.push({
            name: 'Farmyard Manure',
            amount: '5-6 tonnes/ha',
            reason: 'Low organic matter'
        });
    }
    
    return recommendations;
}

// Display Fertilizer Recommendations
function displayFertilizerRecommendations(recommendations) {
    const container = document.getElementById('fertilizer-recommendations');
    container.innerHTML = '';
    
    recommendations.forEach(rec => {
        const item = document.createElement('div');
        item.className = 'recommendation-item';
        item.innerHTML = `
            <i class="fas fa-flask"></i>
            <div>
                <h4>${rec.name} (${rec.amount})</h4>
                <p>${rec.reason}</p>
            </div>
        `;
        container.appendChild(item);
    });
}

// Handle Soil File Upload
function handleSoilFileUpload(file) {
    // In a real implementation, you would send the file to your backend for analysis
    // For demo purposes, we'll simulate the process
    showNotification('Analyzing soil report...', 'info');
    
    setTimeout(() => {
        // Simulate analysis result
        const analysisResult = {
            ph: 6.5,
            nitrogen: 42,
            phosphorus: 25,
            potassium: 175,
            organic_matter: 2.2,
            texture: 'Sandy Loam'
        };
        
        displaySoilData(analysisResult);
        generateSoilRecommendations(analysisResult);
        showNotification('Soil analysis complete!', 'success');
    }, 2000);
}

// Show Manual Test Form
function showManualTestForm() {
    // In a real implementation, you would show a form for manual input
    // For demo purposes, we'll use prompt dialogs
    const ph = parseFloat(prompt('Enter pH level (e.g., 6.5):'));
    const nitrogen = parseFloat(prompt('Enter Nitrogen (kg/ha):'));
    const phosphorus = parseFloat(prompt('Enter Phosphorus (kg/ha):'));
    const potassium = parseFloat(prompt('Enter Potassium (kg/ha):'));
    
    if (!isNaN(ph) && !isNaN(nitrogen) && !isNaN(phosphorus) && !isNaN(potassium)) {
        const manualData = {
            ph,
            nitrogen,
            phosphorus,
            potassium,
            organic_matter: 2.0, // Default value
            texture: 'Loamy' // Default value
        };
        
        displaySoilData(manualData);
        generateSoilRecommendations(manualData);
        showNotification('Soil data updated!', 'success');
    } else {
        showNotification('Invalid input values', 'error');
    }
}

// Add suitability badge styles
const suitabilityStyles = document.createElement('style');
suitabilityStyles.textContent = `
    .suitability-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 5px;
    }
    
    .suitability-high {
        background-color: rgba(76, 175, 80, 0.2);
        color: #4CAF50;
    }
    
    .suitability-medium {
        background-color: rgba(255, 152, 0, 0.2);
        color: #FF9800;
    }
    
    .suitability-low {
        background-color: rgba(244, 67, 54, 0.2);
        color: #F44336;
    }
`;
document.head.appendChild(suitabilityStyles);