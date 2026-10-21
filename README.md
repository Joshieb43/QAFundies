<div align="center">

# 🧪 QA Testing Fundamentals

**A free, open study hub for learning software quality assurance, built with Streamlit.**

Learn the core concepts, practice with interactive tools, and go deeper with 23 hand-picked free resources.

![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/streamlit-1.36%2B-FF4B4B?logo=streamlit&logoColor=white)
![Cost](https://img.shields.io/badge/cost-free-brightgreen)

</div>

---

## ✨ Features

| Page | What you get |
| --- | --- |
| 🏠 **Home** | A 7-step learning path from vocabulary to automation, plus three "start here" resources |
| 📚 **Learn by topic** | 9 core topics, each with a plain-language summary, key points and related sources |
| 🛠️ **Boundary value generator** | Enter a valid range and get the test values you'd use (on the *Test design techniques* topic) |
| 🔗 **Source library** | Search and filter all 23 sources by type, level and topic; switch between cards and a table; export to CSV |
| 📖 **Glossary** | 23 essential testing terms with instant search |
| ✅ **Quiz** | 10 shuffled questions with scoring and an explanation for every answer |

### Topics covered

1. What is testing & why it matters (the seven testing principles)
2. Testing across the SDLC (STLC)
3. Test levels
4. Test types
5. Static vs dynamic testing
6. Test design techniques
7. Test cases, bugs & reporting
8. Manual, exploratory & automated testing
9. Risk-based testing & metrics

### Where the sources come from

Every linked resource is free to access, though a few ask for a free sign-up. They include:

- **Foundations:** the ISTQB CTFL syllabus and glossary, and the BBST course materials
- **Strategy:** Martin Fowler's *Practical Test Pyramid*, *Software Engineering at Google*, and the Google Testing Blog
- **Exploratory testing:** Elisabeth Hendrickson's Test Heuristics Cheat Sheet, Rapid Software Testing, and Ministry of Testing
- **Automation:** Test Automation University, and the Selenium, Playwright, Cypress and Postman docs
- **Non-functional testing:** k6, JMeter, the OWASP Web Security Testing Guide, and W3C accessibility evaluation

---

## 🚀 Quick start

You'll need **Python 3.9 or newer**.

```bash
# 1. Get the code
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>

# 2. (Optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**.

---

## ☁️ Deploy for free

The app runs on [Streamlit Community Cloud](https://share.streamlit.io) at no cost.

1. Push `app.py` and `requirements.txt` to a **public** GitHub repository.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
3. Click **Create app**, choose your repository and branch, and set the main file to `app.py`.
4. Click **Deploy**. A few minutes later you'll have a public URL like `https://your-app-name.streamlit.app`.

Every push to that branch redeploys the app automatically.

---

## 🗂️ Project structure

```
.
├── app.py             # The whole app: content data at the top, page layouts below
├── requirements.txt   # Python dependencies (streamlit, pandas)
└── README.md          # You are here
```

`app.py` is split into two halves:

1. **Content** (`TOPICS`, `SOURCES`, `GLOSSARY`, `QUIZ`): plain Python lists and dictionaries.
2. **Presentation**: the sidebar and one `if/elif` block per page, which read the content and draw it.

You can change almost everything by editing the content alone, without touching the page code.

---

## 🛠️ Customizing

### Add a source

Append a dictionary to `SOURCES`:

```python
{
    "title": "My favorite testing article",
    "url": "https://example.com/article",
    "provider": "Author or site name",
    "topics": ["Test design techniques"],  # must match names in TOPICS exactly
    "type": "Article",                      # Course | Article | Reference | Video/Community | Tool docs
    "level": "Beginner",                    # Beginner | Intermediate | Advanced
    "note": "One line on why it's worth reading.",
},
```

### Add a topic

Add an entry to `TOPICS`, then list that topic name in the `topics` field of any related sources:

```python
"Mobile testing": {
    "summary": "A short paragraph explaining the topic.",
    "key_points": [
        "First key idea.",
        "Second key idea.",
    ],
},
```

### Add a quiz question

Append to `QUIZ`. `answer` is the **zero-based position** of the correct option, so `1` means the second option:

```python
{
    "q": "Which technique tests the edges of input ranges?",
    "options": ["Error guessing", "Boundary value analysis", "Decision tables", "Exploratory testing"],
    "answer": 1,
    "why": "Boundary value analysis focuses on values at and around the edges of partitions.",
},
```

### Add a glossary term

```python
GLOSSARY["Test charter"] = "A statement of test objectives and ideas used to guide an exploratory session."
```

The counts on the Home page and in the sidebar update automatically.

---

## 🧭 Suggested study path

1. **Learn the vocabulary.** Skim the Glossary and the *What is testing* topic.
2. **Study the foundations.** Read the ISTQB CTFL syllabus.
3. **Master test design.** Practice equivalence partitioning and boundary values with the built-in generator.
4. **Write tests & bug reports.** Draft test cases and bug reports for an app you use daily.
5. **Explore.** Run a 30-minute exploratory session with the Test Heuristics Cheat Sheet.
6. **Automate.** Take a beginner course on Test Automation University.
7. **Check yourself.** Take the quiz here, then the official ISTQB sample exam.

---

## 🤝 Contributing

Suggestions for new sources, topics or quiz questions are welcome. Open an issue or a pull request. When you add a source, please:

- Make sure it's **free** to access.
- Check that the link works.
- Tag it with at least one existing topic.

---

## 🙏 Acknowledgements

All linked content belongs to its respective authors and publishers. This app only links to their work. Built with [Streamlit](https://streamlit.io) and [pandas](https://pandas.pydata.org).
