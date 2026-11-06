# LLM API AI Chat Application

A Streamlit chatbot powered by OpenAI, with session chat history, custom system instructions, model controls, token usage, and safe error messages.

## Setup

1. Revoke any exposed API key and create a new one at https://platform.openai.com/api-keys
2. `python -m pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and replace the placeholder with your **new** API key.
4. `streamlit run app.py`

Do not commit `.env` or secrets. The `.gitignore` protects local secrets.

## Deploy

Push the source files to GitHub (without `.env`). Deploy the repository using https://share.streamlit.io/ and set `OPENAI_API_KEY` in Streamlit app secrets using TOML format:

```toml
OPENAI_API_KEY = "your-new-key"
```

The app reads Streamlit secrets on deployment and `.env` locally.

## Limitations

History is session-only, not stored in SQLite. The app does not yet implement JSON structured outputs or dollar cost estimates. Token totals are provided from API usage metadata. Do not expose a paid API key in client-side code.
