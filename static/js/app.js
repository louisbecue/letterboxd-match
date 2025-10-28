document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form[action="/compare"]');
  if (!form) return;

  form.addEventListener('submit', () => {
    document.body.classList.add('loading');
  });
});

/**
 * Switch between Solo and Duo modes
 * @param {string} mode - 'solo' or 'duo'
 */
function switchMode(mode) {
    // Remove active class from all buttons and forms
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelectorAll('.mode-form').forEach(form => {
        form.classList.remove('active');
    });
    
    // Add active class to selected mode
    if (mode === 'solo') {
        document.getElementById('solo-mode-btn').classList.add('active');
        document.getElementById('solo-form').classList.add('active');
    } else if (mode === 'duo') {
        document.getElementById('duo-mode-btn').classList.add('active');
        document.getElementById('duo-form').classList.add('active');
    }
}

/**
 * Initialize mode functionality when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Set default mode to solo
    switchMode('solo');
    
    // Add form submission handlers for loading overlay
    const forms = document.querySelectorAll('.mode-form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const loadingOverlay = document.getElementById('loading-overlay');
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex';
            }
        });
    });
    
    // Add keyboard navigation for mode buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                btn.click();
            }
        });
    });
});

/**
 * Handle form validation
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '#ddd';
        }
    });
    
    return isValid;
}

// Add form validation on submit
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('solo-form').addEventListener('submit', function(e) {
        if (!validateForm('solo-form')) {
            e.preventDefault();
        }
    });
    
    document.getElementById('duo-form').addEventListener('submit', function(e) {
        if (!validateForm('duo-form')) {
            e.preventDefault();
        }
    });
});