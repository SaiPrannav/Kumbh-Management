// Configuration - Update these with your backend API details
const API_BASE_URL = 'http://your-backend-api.com/api'; // Replace with your actual backend URL

// Utility function for making API requests
async function makeApiRequest(endpoint, method, data = null) {
    const url = `${API_BASE_URL}/${endpoint}`;
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`API request failed with status ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API request error:', error);
        throw error;
    }
}

// ==================== PILGRIM REGISTRATION FORM ====================
function initPilgrimRegistration() {
    const form = document.querySelector('.register-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Collect form data using exact field names from HTML
        const formData = {
            fullname: form.fullname.value,
            age: form.age.value,
            gender: form.gender.value,
            phone: form.phone.value,
            email: form.email.value,
            address: form.address.value,
            emergency_name: form.emergency_name.value,
            emergency_number: form.emergency_number.value,
            medical: form.medical.value
        };

        try {
            // UI feedback while processing
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Registering...';

            // Backend integration point - adjust endpoint as needed
            const response = await makeApiRequest('pilgrims/register', 'POST', formData);
            
            // Success handling
            alert(`Registration successful! Your ID: ${response.id || 'N/A'}`);
            form.reset();
            
            // Optional: Redirect or update UI
            // window.location.href = 'success.html';
            
        } catch (error) {
            console.error('Registration error:', error);
            alert('Registration failed. Please try again.');
        } finally {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Register';
            }
        }
    });
}

// ==================== INCIDENT REPORTING FORM ====================
function initIncidentReporting() {
    const form = document.querySelector('.incident-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Collect form data using exact field names from HTML
        const formData = {
            incidentType: form.incidentType.value,
            location: form.location.value,
            dateTime: form.dateTime.value,
            reportedBy: form.reportedBy.value,
            status: form.status.value,
            assignedAuthority: form.assignedAuthority.value
        };

        try {
            // UI feedback while processing
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Submitting...';

            // Backend integration point - adjust endpoint as needed
            const response = await makeApiRequest('incidents/report', 'POST', formData);
            
            // Success handling
            alert(`Incident reported successfully! Case ID: ${response.caseId || 'N/A'}`);
            form.reset();
            
        } catch (error) {
            console.error('Incident reporting error:', error);
            alert('Failed to submit incident report. Please try again.');
        } finally {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Report';
            }
        }
    });
}

// ==================== LOST AND FOUND FORM ====================
function initLostAndFound() {
    const form = document.querySelector('.lost-found-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Collect form data using exact field names from HTML
        const formData = {
            name: form.name.value,
            contact: form.contact.value,
            email: form.email.value,
            itemType: form.itemType.value,
            description: form.description.value,
            location: form.location.value,
            date: form.date.value
        };

        try {
            // UI feedback while processing
            const submitButton = form.querySelector('button[type="submit"]');
            submitButton.disabled = true;
            submitButton.textContent = 'Processing...';

            // Backend integration point - adjust endpoint as needed
            const response = await makeApiRequest('lostfound/report', 'POST', formData);
            
            // Success handling
            alert(`Report submitted successfully! Reference ID: ${response.referenceId || 'N/A'}`);
            form.reset();
            
        } catch (error) {
            console.error('Lost & Found reporting error:', error);
            alert('Failed to submit report. Please try again.');
        } finally {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Report';
            }
        }
    });
}

// ==================== INITIALIZE ALL FORMS ====================
document.addEventListener('DOMContentLoaded', () => {
    initPilgrimRegistration();
    initIncidentReporting();
    initLostAndFound();
});