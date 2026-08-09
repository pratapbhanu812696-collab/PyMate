# 🤖 PyMate - Smart Chatbot

A Python chatbot that goes beyond simple keyword matching — uses **ML-based intent detection** (TF-IDF + Cosine Similarity) to understand user queries, with live weather, shopping search, GATE exam guidance, chat history persistence, and logging.

## Features

- 🧠 **ML-based Intent Detection** — TF-IDF + Cosine Similarity (scikit-learn) instead of hardcoded keyword matching. Understands paraphrased/similar sentences.
- 🌦️ **Live Weather** — Real-time weather via the free Open-Meteo API (no key required).
- 🛒 **Shopping Search Links** — Generates direct Amazon/Flipkart search links for any product query.
- 🎓 **GATE Exam Guidance** — Branch-wise (CSE/ECE/Mechanical) subjects, tips, and book recommendations.
- 💾 **Chat History Persistence** — SQLite database stores conversations per session.
- 📝 **Logging** — All interactions and errors are logged to `pymate.log` for debugging.
- ✅ **Unit Tested** — 11+ test cases covering intent classification, feature handlers, and database ops.
- 🐳 **Dockerized** — Ready for containerized deployment.

## Architecture

```
app.py                 → Streamlit UI layer ONLY (no business logic)
handlers.py             → Core business logic (weather, shopping, GATE, routing)
intent_classifier.py    → ML-based intent detection (TF-IDF + Cosine Similarity)
database.py              → SQLite persistence layer
tests/test_pymate.py    → Unit tests (pytest)
Dockerfile               → Container definition
```

This separation of UI / business logic / ML / data layers follows standard software engineering practice and makes each part independently testable.

## Run Locally in VS Code

```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at `http://localhost:8501`.

## Run Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Run with Docker

```bash
docker build -t pymate .
docker run -p 8501:8501 pymate
```

## Deploy on Streamlit Community Cloud (Free, Easiest)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Sign in with GitHub, select your repo, set main file to `app.py`.
4. Click Deploy.

## Deploy on Render (Free)

1. Push this folder to a GitHub repository.
2. Go to [render.com](https://render.com) → New → Web Service.
3. Connect your GitHub repo.
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy — Render will give you a live URL.

## Customize

Add new intents by editing `INTENT_EXAMPLES` in `intent_classifier.py`:
```python
"college": ["what college do you study at", "tell me about your college"],
```
Then add matching responses in `handlers.py`'s `responses` dictionary.

## Tech Stack

- **Language:** Python 3.9+
- **Web Framework:** Streamlit
- **ML:** scikit-learn (TF-IDF, Cosine Similarity)
- **Database:** SQLite
- **Testing:** pytest
- **Containerization:** Docker

---
Built by **Bhanu Pratap Singh**
