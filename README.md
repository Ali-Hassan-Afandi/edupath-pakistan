# 🎓 EduPath Pakistan

AI-powered education and career guidance for Pakistani students.

## Features
- Student profile
- Personalized AI education report
- 90-day action plan
- AI counselor
- PDF and TXT report downloads
- Groq API
- Streamlit UI

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your-key"
GROQ_MODEL = "openai/gpt-oss-120b"
```

Never commit `secrets.toml` to GitHub.

## Streamlit Community Cloud
Push the repository to GitHub, create a new Streamlit app, select `app.py`,
then add the same secrets in the app's Secrets settings.
