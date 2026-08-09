# 🤖 PyBot - Simple Rule-Based Chatbot

A simple keyword-matching chatbot built in Python, with both a CLI version (for local/VS Code use) and a web version (Streamlit, for deployment).

## Files

- `app.py` — Streamlit web app (use this for deployment)
- `chatbot_cli.py` — Command-line version (run directly in VS Code terminal)
- `requirements.txt` — Python dependencies

## Run Locally in VS Code

**CLI version (no dependencies needed):**
```bash
python chatbot_cli.py
```

**Web version (Streamlit):**
```bash
pip install -r requirements.txt
streamlit run app.py
```
This opens the chatbot in your browser at `http://localhost:8501`.

## Deploy on Render (Free)

1. Push this folder to a GitHub repository.
2. Go to [render.com](https://render.com) → New → Web Service.
3. Connect your GitHub repo.
4. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
5. Deploy — Render will give you a live URL.

## Deploy on Streamlit Community Cloud (Free, Easiest)

1. Push this folder to a GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Sign in with GitHub, select your repo, set main file to `app.py`.
4. Click Deploy.

## Customize

Add more keywords/responses by editing the `responses` dictionary in `app.py` or `chatbot_cli.py`:
```python
"college": ["I study AI & ML at IMS Engineering College!"],
```
