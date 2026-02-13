# Email Composer Agent

A production-structured Email Composer Agent built using **Python**, **FastAPI**, and **Google Gemini (gemini-2.0-flash)**.

This system automatically:

* Generates professional emails using Gemini
* Extracts sender and recipient names from task context
* Applies deterministic placeholder resolution
* Sends multipart (HTML + plain text) emails via SMTP
* Provides both REST API and simple Web UI interfaces

---

## 🚀 Features

### ✅ AI-Powered Email Composition

* Uses `google-genai` SDK
* Model: `gemini-2.0-flash`
* Deterministic structured JSON output
* Strict output enforcement (no conversational drift)

### ✅ Structured Name Extraction (LLM-Driven)

* Gemini extracts:

  * `recipient_name`
  * `sender_name`
* Backend applies fallback logic if names are missing

### ✅ Placeholder Rendering System

* Supports only:

  * `{{recipient_name}}`
  * `{{sender_name}}`
* Normalizes LLM formatting variations
* Fails fast if unresolved placeholders exist

### ✅ Multipart Email Sending

* HTML formatted email
* Plain text fallback
* TLS-secured SMTP
* Retry handling

### ✅ REST API

* `/compose-and-send` – Generate & send email
* `/health` – Service health check
* Swagger UI available at `/docs`

### ✅ Simple Web UI

* Clean form interface
* Direct compose & send
* Success/error feedback

---

## 🏗️ Project Architecture

```
FastAPI Layer
      ↓
Orchestrator Service
      ↓
Gemini Email Generator (LLM)
      ↓
Placeholder Renderer
      ↓
SMTP Sender (HTML + Text)
```

Clear separation of concerns:

* LLM handles NLP
* Backend handles logic
* Renderer handles deterministic replacement
* SMTP handles delivery

---

## 📂 Project Structure

```
email_composer_agent/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── services/
│   │   └── orchestrator.py
│   │
│   ├── llm/
│   │   └── gemini_client.py
│   │
│   ├── email/
│   │   ├── sender.py
│   │   └── formatter.py
│   │
│   └── utils/
│       └── logger.py
│
├── .env
├── pyproject.toml
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Install uv

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 2️⃣ Install Dependencies

```bash
uv sync
```

### 3️⃣ Configure Environment Variables

Create `.env` file:

```
GEMINI_API_KEY=your_gemini_api_key

SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

> ⚠️ Use an App Password for Gmail.

---

## ▶️ Running the Application

### Run API Server

```bash
uv run uvicorn app.main:app --reload
```

Access:

* API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Web UI: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📬 Example API Request

POST `/compose-and-send`

```json
{
  "to_email": "recipient@example.com",
  "task": "Write a formal leave request to Professor Sharma from Arjun for two days.",
  "tone": "formal"
}
```

Response:

```json
{
  "status": "sent",
  "subject": "Leave Request for Two Days",
  "recipient": "recipient@example.com"
}
```

---

## 🧠 Name Resolution Logic

Priority order:

### Recipient Name

1. Extracted by Gemini
2. Fallback → email prefix before `@`

### Sender Name

1. Explicit sender_name field (if provided)
2. Extracted by Gemini
3. Fallback → email prefix before `@`

This ensures deterministic behavior even if the LLM does not extract names.

---

## 🛡️ Security Considerations

* API keys stored in `.env`
* No secrets committed to repository
* TLS-enabled SMTP
* Strict JSON enforcement
* Placeholder validation before sending

---

## 🧪 Testing Tips

Use local SMTP debug server:

```bash
python -m smtpd -c DebuggingServer -n localhost:1025
```

Update `.env` accordingly for testing.

---

## 🔮 Future Enhancements

* Authentication (JWT / API Key)
* Rate limiting
* Async processing
* Background task queue (Celery / Redis)
* Email scheduling
* Attachment support
* Template presets
* Docker deployment
* CI/CD integration

---

## 📌 Tech Stack

* Python 3.11+
* FastAPI
* uv (package manager)
* google-genai SDK
* Gemini 2.0 Flash
* SMTP (TLS)
* Jinja2 (UI rendering)
* Pydantic v2

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Pranav S Kadagadakai

---

## ⭐ Contribution

Pull requests and improvements are welcome.

---

**Email Composer Agent – AI-powered, structured, deterministic email generation and delivery system.**
