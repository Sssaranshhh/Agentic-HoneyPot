# Agentic HoneyPot 
An autonomous AI agent designed to waste scammers' time while extracting actionable intelligence. 

This system acts as a "naive elderly" persona to engage scammers in prolonged conversations, extracting payment details (UPI IDs, bank accounts) and phishing links, which are then logged for reporting.

## 🚀 Features

- **Automated Scam Detection**: Analyzes incoming messages for scam keywords (e.g., "lottery", "urgent", "verify").
- **Adaptive Persona**: Simulates a "naive elderly" victim who is confused, compliant yet slow, or hesitating, forcing the scammer to invest more time.
- **Intelligence Extraction**: Regex-based extraction of:
  - UPI IDs (e.g., `scammer@upi`)
  - Bank Account Numbers
  - Phishing URLs
- **Optimized API**: Fast-path response generation ensures low latency for real-time engagement.
- **Robust Deployment**: Production-ready Flask app with Gunicorn, ready for Render.

## 🛠️ Tech Stack

- **Language**: Python 3.11
- **Framework**: Flask
- **Server**: Gunicorn
- **Deployment**: Render (Infrastructure as Code via `render.yaml`)

## 📦 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agentic-honeypot.git
   cd agentic-honeypot
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running Locally

### Option 1: Run the API Server
```bash
python app.py
```
 The API will start on `http://localhost:5000`.

### Option 2: Run the Simulation (Mock Scammer)
```bash
python main.py
```
This runs a local loop where a mock scammer interacts with the agent in the console.

## 🔗 API Documentation

### POST `/chat`

**Headers:**
- `x-api-key`: `hackathon-2026-secret` (or set via `HONEYPOT_API_KEY` env var)
- `Content-Type`: `application/json`

**Request Body:**
```json
{
  "sessionId": "unique-session-id",
  "message": {
    "text": "Your bank account will be blocked. Verify immediately.",
    "sender": "scammer",
    "timestamp": 1769776085000
  }
}
```

**Response:**
```json
{
  "status": "success",
  "reply": "Oh my goodness! Is this really true? I never win anything!"
}
```

## ☁️ Deployment (Render)

This project includes a `render.yaml` for automatic deployment on Render.

1. Connect your GitHub repository to Render.
2. Select "Blueprints" and chose this repository.
3. Render will automatically detect `render.yaml` and configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2`
   - **Environment Variables**: `HONEYPOT_API_KEY`, `PYTHON_VERSION`.

## 🛡️ License

MIT License
