# 🤖 PyMate - Smart Chatbot

A Python chatbot that goes beyond simple keyword matching — uses **ML-based intent detection** (TF-IDF + Cosine Similarity) to understand user queries, with live weather, shopping search, GATE exam guidance, chat history persistence, and logging.

**Live Application:** [https://pymate.onrender.com/](https://pymate.onrender.com/)

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
