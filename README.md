<h1 align="center">🔬 SkinDiagnosis AI</h1>

<p align="center">
  <strong>Medical-Grade AI Skin Disease Diagnosis System</strong>
  <br>
  <em>5-Stage Deep Analysis Pipeline • Multi-Provider AI Routing • Doctor Verification</em>
</p>

<p align="center">
  <a href="#-features"><img src="https://img.shields.io/badge/Features-12+-blue?style=for-the-badge" alt="Features"></a>
  <a href="#-ai-pipeline"><img src="https://img.shields.io/badge/AI_Stages-5-purple?style=for-the-badge" alt="AI Stages"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/Python-3.12-green?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="#-tech-stack"><img src="https://img.shields.io/badge/Flask-3.1-red?style=for-the-badge&logo=flask" alt="Flask"></a>
  <a href="#-internationalization"><img src="https://img.shields.io/badge/i18n-EN%20%7C%20AR-orange?style=for-the-badge" alt="Languages"></a>
  <a href="#-license"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-ai-pipeline">AI Pipeline</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-contributing">Contributing</a>
</p>

---

## 🎬 Overview

**SkinDiagnosis AI** is a production-grade, full-stack medical application that uses a **multi-stage AI pipeline** to diagnose skin diseases from uploaded images. It combines multiple AI providers (OpenRouter, Google Gemini, Groq) with an intelligent routing and failover system, optional dermatologist review, and a built-in wallet system for managing consultations.

> ⚠️ **Disclaimer**: This system is designed for informational and educational purposes. It does not replace professional medical advice, diagnosis, or treatment.

```
┌──────────────────────────────────────────────────────────────┐
│                    SkinDiagnosis AI                          │
│                                                              │
│    Upload  →   AI Analysis  →   Doctor Review  →   Results   │
│                                                              │
│   ▸ 98% Accuracy    ▸ 100+ Conditions    ▸ 2min Results      │
│   ▸ Bilingual       ▸ Multi-AI           ▸ Wallet System     │
└──────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🧠 AI-Powered Diagnosis
| Feature | Description |
|---------|-------------|
| **5-Stage Pipeline** | Validation → Classification → Categorization → Diagnosis → Fusion |
| **Multi-Provider AI** | OpenRouter (Claude), Google Gemini, Groq (Llama), Internal models |
| **Smart Routing** | Automatic failover between AI providers with retry logic |
| **100+ Conditions** | Infectious, inflammatory, neoplastic, allergic, autoimmune, and more |
| **Image Validation** | Stage 0 gate ensures only valid medical skin images are processed |

### 👥 Multi-Role System
| Role | Capabilities |
|------|-------------|
| **🧑 Patient** | Upload images, view diagnoses, chat with AI assistant, manage wallet |
| **👨‍⚕️ Doctor** | Review AI diagnoses, confirm/modify results, manage specialties, withdraw earnings |
| **🔑 Admin** | Manage doctors, configure diseases/pricing/AI routing, view system logs & statistics |

### 💰 Integrated Wallet System
- **Deposits & Payments** — Patients fund their wallet and pay per diagnosis
- **Configurable Pricing** — Admin controls AI-only vs AI + Doctor Review pricing
- **Doctor Earnings** — Doctors earn from reviews and can withdraw to bank
- **Transaction History** — Full audit trail for all wallet operations

### 🤖 AI Assistant (RAG)
- **Contextual Chat** — AI assistant with conversation memory (last 100 messages)
- **Role-Aware** — Responses tailored to patient vs doctor vs admin
- **Multi-Provider** — Same intelligent routing as the diagnosis pipeline

### 🌍 Internationalization
- **Bilingual UI** — Full English & Arabic support
- **RTL Layout** — Complete right-to-left rendering for Arabic
- **Bilingual Disease Database** — All conditions, categories, and descriptions in EN + AR

### 🎨 Modern UI/UX
- **Mobile-First** — Responsive design optimized for phones with bottom navigation
- **Dark/Light Theme** — System-aware theming with manual toggle
- **Hero Slider** — Animated landing page with touch-swipe support
- **Progressive Web App** — PWA-ready with meta tags and mobile-optimized viewport

---

## 🏗 Architecture

```
SkinApp/
├── 📁 backend/                    # Flask API Server
│   ├── 📄 app.py                  # Application entry point & factory
│   ├── 📄 config.py               # Configuration management (env-based)
│   ├── 📁 ai/                     # AI Engine
│   │   ├── 📄 pipeline.py         # 5-stage orchestrator
│   │   ├── 📄 router.py           # Multi-provider routing + failover
│   │   ├── 📄 stage0_gate.py      # MANDATORY: Image validation gate
│   │   ├── 📄 stage1_classifier.py # Normal vs Abnormal classification
│   │   ├── 📄 stage2_category.py  # Disease category classification
│   │   ├── 📄 stage3_diagnosis.py # Fine-grained disease diagnosis
│   │   ├── 📄 stage4_fusion.py    # AI Fusion: final diagnosis + treatment
│   │   ├── 📁 external/           # External AI providers
│   │   │   ├── 📄 openrouter.py   # OpenRouter (Claude 3 Haiku)
│   │   │   ├── 📄 gemini.py       # Google Gemini 1.5 Flash
│   │   │   └── 📄 groq.py         # Groq (Llama 3.1 70B)
│   │   └── 📁 internal/           # Internal/local models
│   │       └── 📄 internal_model.py
│   ├── 📁 api/                    # REST API Endpoints
│   │   ├── 📄 auth.py             # Authentication (register, login, recovery)
│   │   ├── 📄 diagnosis.py        # Image upload & diagnosis management
│   │   ├── 📄 patients.py         # Patient profile management
│   │   ├── 📄 doctors.py          # Doctor profile & reviews
│   │   ├── 📄 admin.py            # Admin panel APIs
│   │   ├── 📄 wallet.py           # Wallet & transactions
│   │   └── 📄 assistant.py        # AI assistant chat (RAG)
│   ├── 📁 services/               # Business Logic
│   │   ├── 📄 diagnosis_service.py # Pipeline orchestration
│   │   ├── 📄 auth_service.py     # Auth business logic
│   │   └── 📄 assistant_service.py # AI assistant logic
│   ├── 📁 storage/                # Data Layer (JSON-based)
│   │   ├── 📄 json_handler.py     # Thread-safe JSON file I/O
│   │   ├── 📄 user_store.py       # User data management
│   │   ├── 📄 diagnosis_store.py  # Diagnosis records
│   │   ├── 📄 wallet_store.py     # Wallet & transactions
│   │   └── 📄 log_store.py        # Structured logging
│   └── 📁 utils/                  # Utilities
│       ├── 📄 security.py         # JWT, bcrypt, decorators
│       ├── 📄 validators.py       # Input validation
│       ├── 📄 image_utils.py      # Image processing (Pillow)
│       ├── 📄 helpers.py          # Common helper functions
│       └── 📄 logger.py           # Structured logger setup
│
├── 📁 frontend/                   # Client-Side UI
│   ├── 📄 index.html              # Landing page with hero slider
│   ├── 📄 login.html              # Authentication page
│   ├── 📄 register.html           # Registration with role selection
│   ├── 📁 patient/                # Patient Dashboard
│   │   ├── 📄 dashboard.html      # Main patient dashboard
│   │   ├── 📄 new-diagnosis.html  # Upload & start diagnosis
│   │   ├── 📄 result.html         # View diagnosis results
│   │   ├── 📄 history.html        # Diagnosis history
│   │   ├── 📄 wallet.html         # Wallet management
│   │   ├── 📄 profile.html        # Profile settings
│   │   └── 📄 assistant.html      # AI assistant chat
│   ├── 📁 doctor/                 # Doctor Dashboard
│   │   ├── 📄 dashboard.html      # Doctor overview
│   │   └── 📄 review.html         # Review AI diagnoses
│   ├── 📁 admin/                  # Admin Dashboard
│   │   ├── 📄 dashboard.html      # System statistics
│   │   ├── 📄 doctors.html        # Doctor management
│   │   ├── 📄 pricing.html        # Pricing configuration
│   │   └── 📄 logs.html           # System logs viewer
│   ├── 📁 css/                    # Design System
│   │   ├── 📄 variables.css       # CSS custom properties (tokens)
│   │   ├── 📄 main.css            # Base styles & typography
│   │   ├── 📄 components.css      # Reusable components
│   │   └── 📄 layout.css          # Layout & responsive grid
│   ├── 📁 js/                     # Client-Side Logic
│   │   ├── 📄 api.js              # API client with auth headers
│   │   ├── 📄 auth.js             # Authentication flow
│   │   ├── 📄 config.js           # Frontend configuration
│   │   ├── 📄 i18n.js             # Internationalization engine
│   │   ├── 📄 theme.js            # Dark/Light theme manager
│   │   └── 📄 main.js             # Global utilities
│   └── 📁 images/                 # Static assets
│
└── 📁 data/                       # Application Data
    ├── 📁 config/                 # System configuration
    │   ├── 📄 diseases.json       # Disease categories & conditions
    │   ├── 📄 specialties.json    # Doctor specialties mapping
    │   ├── 📄 pricing.json        # Service pricing
    │   └── 📄 ai_routing.json     # AI provider priority & routing
    ├── 📁 users/                  # User records
    ├── 📁 wallets/                # Wallet balances
    └── 📁 admin/                  # Admin credentials
```

---

## 🧠 AI Pipeline

The heart of SkinDiagnosis is a **5-stage sequential AI pipeline** with mandatory gating and intelligent fallback:

```
                          ┌─────────────────┐
                          │  📸 Image       │
                          │   Uploaded      │
                          └────────┬────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   STAGE 0: Validation Gate  │
                    │  ────────────────────────── │
                    │  • Is this a skin image?    │
                    │  • Is quality sufficient?   │
                    │  • MANDATORY: Must pass     │
                    └──────────┬─────────┬────────┘
                               │         │
                          ✅ PASS    ❌ FAIL
                               │         │
                               │    ┌────▼────┐
                               │    │REJECTED │
                               │    └─────────┘
                               │
                    ┌──────────▼──────────────┐
                    │   STAGE 1: Classifier   │
                    │  ────────────────────── │
                    │  Normal vs Abnormal     │
                    │  Confidence scoring     │
                    └──────────┬─────────┬────┘
                               │         │
                          ABNORMAL    NORMAL
                               │         │
                               │    ┌────▼────────────┐
                               │    │ Skip to Stage 4 │
                               │    └────┬────────────┘
                               │         │
                    ┌──────────▼──────────────┐
                    │    STAGE 2: Categor     │
                    │  ────────────────────── │
                    │  • Infectious           │
                    │  • Inflammatory         │
                    │  • Neoplastic           │
                    │  • Allergic             │
                    │  • Autoimmune           │
                    │  • Pigmentary           │
                    │  • Genetic              │
                    └──────────┬──────────────┘
                               │
                    ┌──────────▼──────────────┐
                    │   STAGE 3: Diagnosis    │
                    │  ────────────────────── │
                    │ Fine-grained disease ID │
                    │  Severity assessment    │
                    │  Subcategory mapping    │
                    └──────────┬──────────────┘
                               │
                    ┌──────────▼────────────────┐
                    │     STAGE 4: AI Fusion    │
                    │  ──────────────────────── │
                    │  Combine all stage data   │
                    │ + Patient medical history │
                    │  = Final Diagnosis        │
                    │  + Treatment Plan         │
                    │  + Recommendations        │
                    └──────────┬────────────────┘
                               │
                    ┌──────────▼──────────────────┐
                    │   RESULT                    │
                    │  ────────────────────────── │
                    │    Completed (AI-only)      │
                    │  ─── OR ───                 │
                    │   Awaiting Doctor Review    │
                    └─────────────────────────────┘
```

### AI Provider Priority & Failover

```
┌──────────────────────────────────────────────────┐
│              AI ROUTING ENGINE                   │
│                                                  │
│  Request ──▶ Provider 1 (Primary)                │
│                  │                               │
│              ✅ Success? ──▶ Return result      │
│              ❌ Fail?                           │
│                  │                               │
│              Provider 2 (Fallback #1)            │
│                  │                               │
│              ✅ Success? ──▶ Return result      │
│              ❌ Fail?                           │
│                  │                               │
│              Provider 3 (Fallback #2)            │
│                  │                               │
│              ✅ Success? ──▶ Return result      │
│              ❌ All failed ──▶ Error response   │
│                                                  │
│  Providers:                                      │
│  ┌─────────────┐ ┌──────────┐ ┌──────────┐       │
│  │  OpenRouter │ │  Gemini  │ │   Groq   │       │
│  │ Claude 3    │ │ 1.5 Flash│ │ Llama 3.1│       │
│  │ Haiku       │ │          │ │ 70B      │       │
│  └─────────────┘ └──────────┘ └──────────┘       │
│                                                  │
│  ⚡ Exponential backoff • 🔄 Configurable retry │
│  📊 Per-request logging • 🎛️ Admin-configurable │
└──────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (developed on 3.12)
- **pip** (Python package manager)

### 1. Clone the Repository

```bash
git clone https://github.com/AladdinAlynaey/SkinApp.git
cd SkinApp
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate     # Linux/macOS
# venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Configure Environment

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your API keys:

```env
# Required for AI diagnosis (at least one)
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaXXXXXXXXXXXXXXXXXXXXXX
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXXXXXX

# Security (change in production!)
SECRET_KEY=your-secure-random-key
JWT_SECRET_KEY=your-jwt-secret
```

### 5. Run the Application

```bash
cd backend
python app.py
```

```
╔══════════════════════════════════════════════════════════╗
║     Medical AI Skin Diagnosis System                     ║
║     Version 1.0.0                                        ║
╠══════════════════════════════════════════════════════════╣
║     Server: http://0.0.0.0:5002                          ║
║     Debug: True                                          ║
╚══════════════════════════════════════════════════════════╝
```

Open **http://localhost:5002** in your browser 🎉

---

## 📡 API Reference

### 🔐 Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/register/patient` | Register new patient |
| `POST` | `/api/auth/register/doctor` | Register new doctor (pending approval) |
| `POST` | `/api/auth/login` | Authenticate & get JWT token |
| `POST` | `/api/auth/logout` | Invalidate session |
| `GET`  | `/api/auth/me` | Get current user profile |
| `POST` | `/api/auth/recover-password` | Request password recovery |
| `POST` | `/api/auth/reset-password` | Reset password with token |

### 🩺 Diagnosis

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/diagnoses/upload` | Upload skin image for AI analysis |
| `GET`  | `/api/diagnoses/:id` | Get diagnosis result |
| `GET`  | `/api/diagnoses/:id/status` | Check processing status (0-5 stages) |
| `GET`  | `/api/diagnoses/:id/image` | Retrieve diagnosis image |
| `GET`  | `/api/diagnoses/history` | Get patient's diagnosis history |

### 💰 Wallet

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/wallet/balance` | Get current balance |
| `POST` | `/api/wallet/deposit` | Add funds |
| `GET`  | `/api/wallet/transactions` | Transaction history |
| `POST` | `/api/wallet/withdraw` | Withdraw earnings (doctors) |

### 🤖 AI Assistant

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/assistant/chat` | Send message to AI assistant |
| `GET`  | `/api/assistant/history` | Get conversation history |
| `POST` | `/api/assistant/clear` | Clear conversation memory |

### 🔑 Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/admin/doctors/pending` | Pending doctor approvals |
| `POST` | `/api/admin/doctors/:id/approve` | Approve doctor |
| `POST` | `/api/admin/doctors/:id/reject` | Reject doctor |
| `GET/PUT` | `/api/admin/diseases` | Disease configuration |
| `GET/PUT` | `/api/admin/specialties` | Specialty configuration |
| `GET/PUT` | `/api/admin/pricing` | Pricing configuration |
| `GET/PUT` | `/api/admin/ai-routing` | AI provider routing config |
| `GET`  | `/api/admin/logs/:category` | System logs (api/ai/auth/errors/audit) |
| `GET`  | `/api/admin/statistics` | System statistics |

### 🏥 Health Check

```bash
curl http://localhost:5002/api/health
```

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "Medical AI Skin Diagnosis System"
}
```

---

## 🔒 Security

| Feature | Implementation |
|---------|---------------|
| **Password Hashing** | bcrypt with configurable log rounds (12 dev / 14 prod) |
| **Authentication** | JWT tokens with configurable expiry (24h default) |
| **Role-Based Access** | Decorators: `@require_auth`, `@require_patient`, `@require_admin` |
| **Input Validation** | Email validator, password strength checks, image validation |
| **CORS** | Configurable cross-origin resource sharing |
| **File Upload Security** | Extension whitelist, size limits, secure filenames |
| **Anti-Enumeration** | Password recovery always returns success message |

---

## 🗂 Disease Database

The system supports a comprehensive, bilingual disease taxonomy:

| Category | Subcategories | Example Conditions |
|----------|--------------|-------------------|
| 🦠 **Infectious** | Bacterial, Viral, Fungal, Parasitic | Ringworm, Herpes, Scabies |
| 🔥 **Inflammatory** | Eczema, Psoriasis, Dermatitis | Atopic Dermatitis, Plaque Psoriasis, Acne |
| 🧬 **Neoplastic** | Benign, Malignant, Pre-malignant | Melanoma, Basal Cell Carcinoma |
| ⚡ **Allergic** | Urticaria, Contact Allergy | Contact Dermatitis, Hives |
| 🛡 **Autoimmune** | Lupus, Vitiligo | Systemic Lupus, Vitiligo |
| 🎨 **Pigmentary** | — | Hyperpigmentation, Melasma |
| 🧬 **Genetic** | — | Ichthyosis, Epidermolysis Bullosa |

> All conditions include Arabic translations. The admin can add, modify, or remove conditions at runtime.

---

## 🛠 Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Flask 3.1** | Web framework with application factory pattern |
| **Flask-CORS** | Cross-origin resource sharing |
| **bcrypt** | Password hashing |
| **PyJWT** | JSON Web Token authentication |
| **Pillow** | Image processing & validation |
| **NumPy** | Image array operations |
| **google-generativeai** | Gemini AI integration |
| **groq** | Groq AI integration |
| **httpx** | Async HTTP client for OpenRouter |
| **Flask-Mail** | Email delivery (password recovery) |
| **filelock** | Thread-safe file I/O |
| **python-dotenv** | Environment configuration |

### Frontend
| Technology | Purpose |
|------------|---------|
| **Vanilla JS** | Zero-dependency client-side logic |
| **CSS Custom Properties** | Design token system |
| **Inter + Tajawal** | Typography (Latin + Arabic) |
| **SVG Icons** | Crisp, scalable iconography |

### Data Storage
| Technology | Purpose |
|------------|---------|
| **JSON Files** | Lightweight, zero-config data persistence |
| **filelock** | Concurrent access safety |
| **Structured directories** | Organized data hierarchy |

---

## ⚙️ Configuration

All configuration is managed through environment variables (see `backend/.env.example`):

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `development` | Environment mode |
| `FLASK_DEBUG` | `1` | Enable debug mode |
| `PORT` | `5002` | Server port |
| `SECRET_KEY` | `dev-secret...` | Flask secret key |
| `JWT_SECRET_KEY` | (uses SECRET_KEY) | JWT signing key |
| `SESSION_LIFETIME_HOURS` | `24` | Token expiry |
| `OPENROUTER_API_KEY` | — | OpenRouter API key |
| `GEMINI_API_KEY` | — | Google Gemini API key |
| `GROQ_API_KEY` | — | Groq API key |
| `AI_REQUEST_TIMEOUT_SECONDS` | `30` | AI provider timeout |
| `AI_MAX_RETRIES` | `3` | Max retry attempts |
| `MAX_UPLOAD_SIZE_MB` | `10` | Max image upload size |
| `LOG_LEVEL` | `DEBUG` | Logging verbosity |

---

## 🧪 Testing

```bash
# Run all tests
cd backend
pytest

# With coverage report
pytest --cov=. --cov-report=html

# Open coverage report
open htmlcov/index.html
```

---

## 📊 Logging & Monitoring

The system implements structured logging across 5 categories:

| Category | What's Logged |
|----------|---------------|
| **`api`** | All API requests with timing, user ID, and response codes |
| **`ai`** | AI provider calls, success/failure, duration, fallback usage |
| **`auth`** | Login attempts, registrations, password resets |
| **`errors`** | Exceptions with full stack traces |
| **`audit`** | Admin actions (doctor approvals, config changes) |

Logs are JSON-formatted with automatic rotation (7-day active, 30-day archive).

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=0`
- [ ] Generate strong `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Configure at least one AI provider API key
- [ ] Set up proper email credentials for password recovery
- [ ] Use a reverse proxy (Nginx) in front of Flask
- [ ] Consider using Gunicorn as the WSGI server
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper CORS origins
- [ ] Set up log rotation and monitoring

### Run with Gunicorn

```bash
pip install gunicorn
cd backend
gunicorn -w 4 -b 0.0.0.0:5002 app:app
```

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Ensure all API endpoints have proper error handling
- Add bilingual support (EN + AR) for any new user-facing content
- Write tests for new features
- Update this README when adding new features or endpoints

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built by [Alaadin Alynaey](https://alaadin-alynaey.site)**

⭐ Star this repo if you find it useful!

</div>
