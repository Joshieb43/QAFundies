# 🧪 QA Testing Fundamentals — Streamlit App

A free study hub for software testing fundamentals: topic summaries, 23 curated free sources, a searchable glossary, a boundary-value generator, and a 10-question quiz.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy for free (Streamlit Community Cloud)

1. Create a public GitHub repo and add `app.py` and `requirements.txt`.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, pick your repo and branch, set the main file to `app.py`, and click **Deploy**.
4. You'll get a free public URL like `https://your-app-name.streamlit.app`.

## Customize

- Add sources: append a dictionary to the `SOURCES` list in `app.py`.
- Add topics: add an entry to `TOPICS`, then tag sources with the topic name.
- Add quiz questions: append to `QUIZ` (`answer` is the zero-based index of the correct option).
