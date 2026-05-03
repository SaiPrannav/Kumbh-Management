// =============================================
// Kumbh Management - Form Submission Handler
// =============================================

const API = window.location.origin; // uses your Railway domain automatically

// ── Utility ──────────────────────────────────

function showMessage(msg, isError = false) {
  let box = document.getElementById("form-message");
  if (!box) {
    box = document.createElement("div");
    box.id = "form-message";
    box.style.cssText = `
      position: fixed; top: 20px; right: 20px; z-index: 9999;
      padding: 14px 24px; border-radius: 8px; font-size: 15px;
      font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
      transition: opacity 0.4s;
    `;
    document.body.appendChild(box);
  }
  box.textContent = msg;
  box.style.background = isError ? "#e74c3c" : "#27ae60";
  box.style.color = "#fff";
  box.style.opacity = "1";
  setTimeout(() => { box.style.opacity = "0"; }, 4000);
}

function generateId(prefix) {
  return prefix + "-" + Math.random().toString(36).substr(2, 8).toUpperCase();
}

async function postJSON(endpoint, body) {
  const res = await fetch(`${API}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Server error ${res.status}`);
  }
  return res.json();
}

// ── Pilgrim Registration (register.html) ──────

const registerForm = document.querySelector(".register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const inputs = registerForm.querySelectorAll("input, select, textarea");

    const [name, age, gender, phone, email, address, emergencyName, emergencyNum, medical] =
      [...inputs].map(i => i.value.trim());

    try {
      const data = await postJSON("/pilgrims/register", {
        Name: name,
        Age: parseInt(age) || null,
        Gender: gender || null,
        Contact_Number: phone,
        Email_Address: email,
        Address: address,
        Emergency_Contact: emergencyNum,
        Medical_Condition: medical || null,
      });
      showMessage(`✅ Registered! Your ID: ${data.id}`);
      registerForm.reset();
    } catch (err) {
      showMessage(`❌ ${err.message}`, true);
    }
  });
}

// ── Lost & Found (lost_found.html) ───────────

const lostForm = document.querySelector(".lost-found-form");
if (lostForm) {
  lostForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const inputs = lostForm.querySelectorAll("input, select, textarea");
    const [name, contact, email, itemType, description, location, date] =
      [...inputs].map(i => i.value.trim());

    try {
      await postJSON("/lost-and-found/report", {
        Lost_Item_Person_ID: generateId("LF"),
        Description: `[${itemType}] ${description}`,
        Date_Time: new Date(date).toISOString(),
        Reported_By: name,
        Availability: true,
        Claim_Status: "Unclaimed",
        Location: location,
      });
      showMessage("✅ Report submitted successfully!");
      lostForm.reset();
    } catch (err) {
      showMessage(`❌ ${err.message}`, true);
    }
  });
}

// ── Incident Reporting (incident.html) ───────

const incidentForm = document.querySelector(".incident-form");
if (incidentForm) {
  incidentForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const type      = document.getElementById("incidentType")?.value;
    const location  = document.getElementById("location")?.value.trim();
    const dateTime  = document.getElementById("dateTime")?.value;
    const reporter  = document.getElementById("reportedBy")?.value.trim();
    const status    = document.getElementById("status")?.value;
    const authority = document.getElementById("assignedAuthority")?.value.trim();

    try {
      await postJSON("/incidents/report", {
        Incident_ID: generateId("INC"),
        Incident_Type: type,
        Date_Time: new Date(dateTime).toISOString(),
        Location: location,
        Reported_By: reporter,
        Status: status,
        Assigned_Authority: authority,
      });
      showMessage("✅ Incident reported successfully!");
      incidentForm.reset();
    } catch (err) {
      showMessage(`❌ ${err.message}`, true);
    }
  });
}
