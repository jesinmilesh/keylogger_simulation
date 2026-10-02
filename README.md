# 🛡️ Secure Payment & Web Interception Awareness Demo

An educational proof-of-concept project designed for academic demonstrations and security awareness training. This project illustrates how web-based input tracking and session monitoring operate in browser environments, highlighting the importance of client-side defenses, Content Security Policies (CSP), and secure authentication.

---

### ⚠️ Disclaimer & Educational Notice

> **IMPORTANT:** This repository is intended strictly for educational, research, and defensive awareness purposes. Unauthorized interception of user data on systems without explicit consent is illegal and unethical. Use this project only in controlled, authorized environments.

---

## 🏗️ Project Architecture

The project is structured into two main components:

```
keylogger_simulation/
├── api/
│   └── index.py          # Vercel Serverless Function entry point
├── clients/
│   ├── index.html        # Secure Payment Checkout Demo Page
│   ├── main.css          # Glassmorphism UI & Layout Styling
│   └── script.js         # Frontend Interaction & Event Listener Logic
├── server/
│   ├── app.py            # Flask Backend Status & Logging Server
│   └── server_details.html # Monitoring Dashboard Interface
├── vercel.json           # Vercel Routing Configuration
├── requirements.txt      # Python Dependencies
└── README.md             # Project Documentation
```

### Component Roles

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Client Frontend** | HTML5 / CSS3 / Vanilla JS | Simulates a secure event payment checkout page with dynamic payment method forms (Card, UPI, Net Banking). |
| **Server Backend** | Python / Flask / Flask-CORS | Provides endpoints (`/log` and `/status`) to monitor active client sessions and render status dashboards. |
| **Vercel Serverless** | Vercel Python Runtime | Serverless deployment entry point routing requests to the Flask application. |

---

## 🚀 Setup & Local Execution

### 1. Prerequisites

Ensure Python 3.x is installed, then install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Running the Server

Start the Flask backend server:

```bash
python server/app.py
```

The server will run locally on `http://127.0.0.1:5000`.

### 3. Running the Client Demo

1. Open `clients/index.html` in any modern web browser.
2. Interact with the payment form (select payment options, type sample data).
3. Open `server/server_details.html` in a browser to view real-time session status updates.

### 4. Deploying to Vercel & CI/CD Pipeline

Any changes made in this repository can be automatically deployed to Vercel in two ways:

#### Option A: Native Vercel Git Integration (Zero Configuration)
1. Push this repository to GitHub (`https://github.com/jesinmilesh/keylogger_simulation.git`).
2. Go to [Vercel Dashboard](https://vercel.com/dashboard) > **Add New...** > **Project** and import this repository.
3. Once imported, **every commit pushed to the `main` branch automatically triggers a new deployment to Vercel**. Pull requests automatically generate preview deployments.

#### Option B: GitHub Actions Workflow (`.github/workflows/deploy.yml`)
If you want automated testing, validation, and CLI-based deployment on every push via GitHub Actions:
1. In your GitHub repository settings, go to **Settings > Secrets and variables > Actions**.
2. Add the following repository secrets:
   - `VERCEL_TOKEN`: Personal Access Token from your [Vercel Account Settings](https://vercel.com/account/tokens).
   - `VERCEL_ORG_ID`: Your Vercel team/user ID (found in `.vercel/project.json` or team settings).
   - `VERCEL_PROJECT_ID`: Your Vercel project ID (found in Vercel project settings).
3. The workflow will automatically validate the Python environment and deploy to production on every push to `main`.

---

## 🛡️ Defensive Mitigations & Best Practices

To protect web applications against unauthorized script execution and client-side interception:

- **Content Security Policy (CSP):** Enforce strict `connect-src` headers to restrict browsers from transmitting data to unapproved endpoints.
- **Multi-Factor Authentication (MFA):** Ensure sensitive actions require out-of-band verification.
- **Password Managers & Autofill:** Utilizing browser autofill reduces direct physical keyboard input.
- **Subresource Integrity (SRI) & Script Auditing:** Regularly audit third-party scripts to prevent unauthorized DOM event listening.
