// API endpoint
const API_URL = '';

// Demo data cache
let demoData = {};

// Load demo data on startup
fetch('/api/demo')
    .then(r => r.json())
    .then(data => {
        demoData = data;
        console.log('Demo data loaded');
    });

// Load demo into form
function loadDemo(type) {
    const demo = demoData[type];
    if (!demo) return;
    
    const data = demo.data;
    const form = document.getElementById('predictionForm');
    
    // Fill all fields
    Object.keys(data).forEach(key => {
        const input = form.querySelector(`[name="${key}"]`);
        if (input) {
            if (input.type === 'checkbox') {
                input.checked = data[key] === 'yes';
            } else {
                input.value = data[key];
            }
        }
    });
    
    // Show notification
    showNotification(`Loaded: ${demo.name}`, 'success');
}

// Handle form submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const data = {};
    
    // Process form data
    formData.forEach((value, key) => {
        data[key] = value;
    });
    
    // Handle checkboxes (convert to yes/no)
    ['schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic'].forEach(field => {
        data[field] = data[field] ? 'yes' : 'no';
    });
    
    // Show loading
    document.getElementById('loading').classList.remove('hidden');
    
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayResults(result);
        } else {
            showNotification('Error: ' + result.error, 'error');
        }
    } catch (error) {
        showNotification('Network error', 'error');
    } finally {
        document.getElementById('loading').classList.add('hidden');
    }
});

// Display results
function displayResults(response) {
    const pred = response.prediction;
    const summary = response.input_summary;
    
    // Update values
    document.getElementById('predictedGrade').textContent = pred.predicted_grade;
    document.getElementById('passProbability').textContent = (pred.pass_probability * 100).toFixed(1) + '%';
    document.getElementById('confidenceLevel').textContent = pred.confidence + ' Confidence';
    document.getElementById('passFail').textContent = pred.pass_fail;
    document.getElementById('riskLevel').textContent = pred.risk_level;
    document.getElementById('adviceText').textContent = pred.advice;
    
    // Update progress bar
    const percent = Math.round(pred.pass_probability * 100);
    document.getElementById('progressPercent').textContent = percent + '%';
    document.getElementById('progressFill').style.width = percent + '%';
    
    // Color coding
    const statusBox = document.getElementById('statusBox');
    const passFailEl = document.getElementById('passFail');
    const riskEl = document.getElementById('riskLevel');
    
    if (pred.pass_fail === 'PASS') {
        passFailEl.classList.add('status-pass');
        passFailEl.classList.remove('status-fail');
        statusBox.style.borderTopColor = 'var(--success)';
    } else {
        passFailEl.classList.add('status-fail');
        passFailEl.classList.remove('status-pass');
        statusBox.style.borderTopColor = 'var(--danger)';
    }
    
    // Risk color
    riskEl.className = 'result-sub';
    if (pred.risk_level.includes('High')) riskEl.classList.add('risk-high');
    else if (pred.risk_level.includes('Medium')) riskEl.classList.add('risk-medium');
    else riskEl.classList.add('risk-low');
    
    // Update summary
    const summaryGrid = document.getElementById('inputSummary');
    summaryGrid.innerHTML = `
        <div class="summary-item">
            <span class="summary-label">Past Grades</span>
            <span class="summary-value">${summary.past_grades}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Study Time</span>
            <span class="summary-value">${summary.study_time}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Absences</span>
            <span class="summary-value">${summary.absences}</span>
        </div>
        <div class="summary-item">
            <span class="summary-label">Past Failures</span>
            <span class="summary-value">${summary.failures}</span>
        </div>
    `;
    
    // Show results card
    document.getElementById('resultsCard').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('resultsCard').scrollIntoView({ behavior: 'smooth' });
}

// Notification helper
function showNotification(message, type) {
    // Simple alert for now - can be enhanced
    console.log(`[${type.toUpperCase()}] ${message}`);
}

// Health check
fetch('/api/health')
    .then(r => r.json())
    .then(data => {
        console.log('API Health:', data);
    });