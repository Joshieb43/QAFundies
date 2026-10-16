"""
QA Testing Fundamentals — a free study hub built with Streamlit.

Run locally:   streamlit run app.py
Deploy free:   push to GitHub, then deploy at https://share.streamlit.io
"""

import random

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="QA Testing Fundamentals",
    page_icon="🧪",
    layout="wide",
)

# ---------------------------------------------------------------------------
# DATA: topics, sources, glossary, quiz
# ---------------------------------------------------------------------------

TOPICS = {
    "What is testing & why it matters": {
        "summary": (
            "Software testing is the process of evaluating a product to find defects, "
            "reduce risk, and build confidence that it meets requirements and user needs. "
            "Quality Assurance (QA) is broader: it covers the *processes* that prevent "
            "defects, while Quality Control (QC) and testing *detect* them."
        ),
        "key_points": [
            "Testing shows the presence of defects, not their absence.",
            "Exhaustive testing is impossible — prioritize by risk.",
            "Early testing (shift-left) saves time and money.",
            "Defects cluster: a few modules usually hold most of the bugs.",
            "Tests wear out (the 'pesticide paradox') — refresh them regularly.",
            "Testing is context dependent: a banking app ≠ a mobile game.",
            "'Absence-of-defects' fallacy: bug-free software can still fail users.",
        ],
    },
    "Testing across the SDLC (STLC)": {
        "summary": (
            "The Software Testing Life Cycle (STLC) runs alongside development: "
            "requirement analysis → test planning → test case design → environment setup "
            "→ test execution → test closure. In Agile and DevOps these activities happen "
            "continuously within each iteration rather than as one long phase."
        ),
        "key_points": [
            "Test planning defines scope, approach, resources, schedule and exit criteria.",
            "Entry criteria say when testing can start; exit criteria say when it's done.",
            "In Agile, testers collaborate on user stories and acceptance criteria up front.",
            "Continuous testing in CI/CD gives fast feedback on every commit.",
        ],
    },
    "Test levels": {
        "summary": (
            "Test levels group activities by what is being tested: individual units, "
            "how they work together, the whole system, and whether it is acceptable "
            "to the business or users."
        ),
        "key_points": [
            "Unit / component testing — smallest testable pieces, usually by developers.",
            "Integration testing — interfaces and interactions between components or systems.",
            "System testing — the complete, integrated product against requirements.",
            "Acceptance testing (UAT, alpha, beta) — is it fit for use by real users?",
            "The Test Pyramid: many fast unit tests, fewer integration tests, few end-to-end tests.",
        ],
    },
    "Test types": {
        "summary": (
            "Test types describe *what quality characteristic* you're checking. "
            "Any type can be applied at any level."
        ),
        "key_points": [
            "Functional — does it do what it should?",
            "Non-functional — performance, security, usability, accessibility, reliability.",
            "Regression — did a change break something that used to work?",
            "Smoke — quick check that the build is stable enough to test further.",
            "Sanity — narrow check that a specific fix or feature works.",
            "Confirmation (re-testing) — verifying that a reported defect is fixed.",
        ],
    },
    "Static vs dynamic testing": {
        "summary": (
            "Static testing examines work products *without running code* — reviews, "
            "walkthroughs, inspections and static analysis tools. Dynamic testing executes "
            "the software and observes behavior."
        ),
        "key_points": [
            "Static testing finds defects early, often in requirements or design.",
            "Review types range from informal to formal inspection.",
            "Static analysis (linters, SAST) catches code smells and security issues automatically.",
        ],
    },
    "Test design techniques": {
        "summary": (
            "Techniques help you choose a small set of tests that find the most defects. "
            "They fall into black-box (behavior-based), white-box (structure-based) and "
            "experience-based approaches."
        ),
        "key_points": [
            "Equivalence partitioning — split inputs into classes that behave the same; test one from each.",
            "Boundary value analysis — bugs hide at edges (min, min-1, max, max+1).",
            "Decision tables — cover combinations of conditions and actions.",
            "State transition testing — valid and invalid moves between states.",
            "Statement & branch coverage — white-box measures of how much code tests exercise.",
            "Error guessing & exploratory testing — use experience and curiosity.",
        ],
    },
    "Test cases, bugs & reporting": {
        "summary": (
            "A good test case is clear, repeatable and traceable to a requirement. "
            "A good bug report lets someone else reproduce the problem quickly."
        ),
        "key_points": [
            "Test case: ID, title, preconditions, steps, test data, expected result.",
            "Bug report: summary, environment, steps to reproduce, expected vs actual, evidence.",
            "Severity = impact on the system; Priority = urgency to fix.",
            "Defect life cycle: New → Assigned → Open → Fixed → Retest → Closed (or Reopened).",
            "Traceability matrix links requirements ↔ tests ↔ defects.",
        ],
    },
    "Manual, exploratory & automated testing": {
        "summary": (
            "Manual and exploratory testing bring human judgment; automation brings speed and "
            "repeatability. Strong teams use both, automating stable, repetitive checks and "
            "exploring where risk and uncertainty are highest."
        ),
        "key_points": [
            "Exploratory testing = simultaneous learning, test design and execution.",
            "Session-based test management uses time-boxed charters.",
            "Automate regression, smoke and data-driven tests first.",
            "Common tools: Selenium, Playwright, Cypress (UI); Postman (API); JMeter, k6 (load).",
        ],
    },
    "Risk-based testing & metrics": {
        "summary": (
            "Risk = likelihood × impact. Risk-based testing focuses effort where failure "
            "would hurt most. Metrics help track progress, but beware of gaming them."
        ),
        "key_points": [
            "Product risks threaten quality; project risks threaten schedule or budget.",
            "Useful metrics: test pass rate, defect density, escaped defects, coverage.",
            "100% code coverage does not mean 100% tested.",
        ],
    },
}

# type: Course | Article | Reference | Video/Community | Tool docs
# level: Beginner | Intermediate | Advanced
SOURCES = [
    # --- Foundations / certification ---
    {
        "title": "ISTQB Certified Tester Foundation Level (CTFL v4.0) syllabus",
        "url": "https://istqb.org/certifications/certified-tester-foundation-level-ctfl-v4-0/",
        "provider": "ISTQB",
        "topics": ["What is testing & why it matters", "Testing across the SDLC (STLC)",
                   "Test levels", "Test types", "Static vs dynamic testing",
                   "Test design techniques", "Risk-based testing & metrics"],
        "type": "Reference",
        "level": "Beginner",
        "note": "The industry-standard foundation syllabus, free to download along with sample exams.",
    },
    {
        "title": "ISTQB Glossary",
        "url": "https://glossary.istqb.org/",
        "provider": "ISTQB",
        "topics": ["What is testing & why it matters"],
        "type": "Reference",
        "level": "Beginner",
        "note": "Searchable definitions of standard testing terms.",
    },
    {
        "title": "BBST — Black Box Software Testing (course materials)",
        "url": "https://bbst.courses/",
        "provider": "Cem Kaner et al.",
        "topics": ["What is testing & why it matters", "Test design techniques",
                   "Test cases, bugs & reporting"],
        "type": "Course",
        "level": "Intermediate",
        "note": "Classic, rigorous course on test foundations, bug advocacy and test design.",
    },
    # --- Strategy / pyramid ---
    {
        "title": "The Practical Test Pyramid",
        "url": "https://martinfowler.com/articles/practical-test-pyramid.html",
        "provider": "Ham Vocke on martinfowler.com",
        "topics": ["Test levels", "Manual, exploratory & automated testing"],
        "type": "Article",
        "level": "Intermediate",
        "note": "The most-cited practical guide to balancing unit, integration and end-to-end tests.",
    },
    {
        "title": "Software Testing Guide (collection)",
        "url": "https://martinfowler.com/testing/",
        "provider": "Martin Fowler",
        "topics": ["Test levels", "Test types"],
        "type": "Article",
        "level": "Intermediate",
        "note": "Short definitions of unit, integration, contract, component and other test categories.",
    },
    {
        "title": "Test Pyramid (bliki)",
        "url": "https://martinfowler.com/bliki/TestPyramid.html",
        "provider": "Martin Fowler",
        "topics": ["Test levels"],
        "type": "Article",
        "level": "Beginner",
        "note": "A two-minute read on why the pyramid has the shape it does.",
    },
    {
        "title": "Software Engineering at Google — testing chapters (free online book)",
        "url": "https://abseil.io/resources/swe-book",
        "provider": "Google / O'Reilly",
        "topics": ["Test levels", "Manual, exploratory & automated testing",
                   "Testing across the SDLC (STLC)"],
        "type": "Reference",
        "level": "Advanced",
        "note": "Chapters 11–14 cover testing culture, unit tests, test doubles and larger tests at scale.",
    },
    {
        "title": "Google Testing Blog",
        "url": "https://testing.googleblog.com/",
        "provider": "Google",
        "topics": ["Manual, exploratory & automated testing", "Test levels"],
        "type": "Article",
        "level": "Intermediate",
        "note": "Includes the bite-sized 'Testing on the Toilet' tips.",
    },
    {
        "title": "Types of software testing",
        "url": "https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing",
        "provider": "Atlassian",
        "topics": ["Test types", "Test levels", "Testing across the SDLC (STLC)"],
        "type": "Article",
        "level": "Beginner",
        "note": "Plain-language overview of test types in a continuous-delivery context.",
    },
    # --- Exploratory / craft ---
    {
        "title": "Test Heuristics Cheat Sheet",
        "url": "https://testobsessed.com/wp-content/uploads/2011/04/testheuristicscheatsheetv1.pdf",
        "provider": "Elisabeth Hendrickson et al.",
        "topics": ["Test design techniques", "Manual, exploratory & automated testing"],
        "type": "Reference",
        "level": "Beginner",
        "note": "One-page list of data types, attacks and heuristics for exploratory testing.",
    },
    {
        "title": "Rapid Software Testing resources",
        "url": "https://www.satisfice.com/",
        "provider": "James Bach / Satisfice",
        "topics": ["Manual, exploratory & automated testing", "Risk-based testing & metrics"],
        "type": "Article",
        "level": "Advanced",
        "note": "Context-driven testing, heuristics and exploratory methodology.",
    },
    {
        "title": "Software Testing Essentials: Resources for Beginners",
        "url": "https://www.ministryoftesting.com/collections/software-testing-essentials-resources-for-beginners",
        "provider": "Ministry of Testing",
        "topics": ["What is testing & why it matters", "Test cases, bugs & reporting"],
        "type": "Video/Community",
        "level": "Beginner",
        "note": "Curated beginner collection from the largest testing community (free account for some content).",
    },
    {
        "title": "Free Learning Resources for Software Testers",
        "url": "https://github.com/gtorchia/FreeLearningResourcesForSoftwareTesters",
        "provider": "GitHub community list",
        "topics": ["What is testing & why it matters", "Manual, exploratory & automated testing"],
        "type": "Reference",
        "level": "Beginner",
        "note": "Crowd-sourced list of free testing courses, talks and articles.",
    },
    # --- Automation ---
    {
        "title": "Test Automation University",
        "url": "https://testautomationu.applitools.com/",
        "provider": "Applitools",
        "topics": ["Manual, exploratory & automated testing"],
        "type": "Course",
        "level": "Beginner",
        "note": "Dozens of free video courses on web, mobile, API and codeless automation.",
    },
    {
        "title": "Setting a Foundation for Successful Test Automation",
        "url": "https://testautomationu.applitools.com/setting-a-foundation-for-successful-test-automation/",
        "provider": "Angie Jones · TAU",
        "topics": ["Manual, exploratory & automated testing", "Risk-based testing & metrics"],
        "type": "Course",
        "level": "Beginner",
        "note": "Strategy-first intro: what to automate, culture, tooling and measuring value.",
    },
    {
        "title": "Selenium documentation",
        "url": "https://www.selenium.dev/documentation/",
        "provider": "Selenium project",
        "topics": ["Manual, exploratory & automated testing"],
        "type": "Tool docs",
        "level": "Intermediate",
        "note": "Official WebDriver docs, including test-practice guidance.",
    },
    {
        "title": "Playwright documentation",
        "url": "https://playwright.dev/docs/intro",
        "provider": "Microsoft",
        "topics": ["Manual, exploratory & automated testing"],
        "type": "Tool docs",
        "level": "Intermediate",
        "note": "Modern cross-browser end-to-end testing framework.",
    },
    {
        "title": "Cypress documentation",
        "url": "https://docs.cypress.io/",
        "provider": "Cypress.io",
        "topics": ["Manual, exploratory & automated testing"],
        "type": "Tool docs",
        "level": "Intermediate",
        "note": "JavaScript end-to-end and component testing.",
    },
    {
        "title": "Postman Learning Center",
        "url": "https://learning.postman.com/",
        "provider": "Postman",
        "topics": ["Test types", "Manual, exploratory & automated testing"],
        "type": "Tool docs",
        "level": "Beginner",
        "note": "API testing basics: requests, assertions, collections and automation.",
    },
    # --- Non-functional ---
    {
        "title": "Grafana k6 documentation",
        "url": "https://grafana.com/docs/k6/latest/",
        "provider": "Grafana Labs",
        "topics": ["Test types"],
        "type": "Tool docs",
        "level": "Intermediate",
        "note": "Load and performance testing, including test-type guides (smoke, load, stress, soak).",
    },
    {
        "title": "Apache JMeter user manual",
        "url": "https://jmeter.apache.org/usermanual/index.html",
        "provider": "Apache Software Foundation",
        "topics": ["Test types"],
        "type": "Tool docs",
        "level": "Intermediate",
        "note": "Open-source load testing tool documentation.",
    },
    {
        "title": "OWASP Web Security Testing Guide",
        "url": "https://owasp.org/www-project-web-security-testing-guide/",
        "provider": "OWASP",
        "topics": ["Test types", "Static vs dynamic testing"],
        "type": "Reference",
        "level": "Advanced",
        "note": "Comprehensive free framework for testing web application security.",
    },
    {
        "title": "W3C Web Accessibility Initiative — evaluating accessibility",
        "url": "https://www.w3.org/WAI/test-evaluate/",
        "provider": "W3C WAI",
        "topics": ["Test types"],
        "type": "Reference",
        "level": "Beginner",
        "note": "How to check websites for accessibility, from quick checks to full WCAG audits.",
    },
]

GLOSSARY = {
    "Bug / Defect": "A flaw in a work product that can cause it to fail to meet requirements.",
    "Error (mistake)": "A human action that produces a defect.",
    "Failure": "An event where the system does not do what is expected, caused by a defect.",
    "Test case": "A set of preconditions, inputs, actions and expected results for a test.",
    "Test suite": "A collection of test cases run together.",
    "Test plan": "Document describing scope, approach, resources and schedule of testing.",
    "Test oracle": "A source used to determine the expected result of a test.",
    "Regression testing": "Re-testing after changes to catch unintended side effects.",
    "Smoke test": "A shallow, wide test confirming the build is stable enough for more testing.",
    "Sanity test": "A narrow, focused check that a specific change works.",
    "Black-box testing": "Testing based on specifications/behavior, without looking at code.",
    "White-box testing": "Testing based on the internal structure of the code.",
    "Equivalence partitioning": "Dividing inputs into groups expected to behave the same way.",
    "Boundary value analysis": "Testing at the edges of equivalence partitions.",
    "Code coverage": "The percentage of code (statements, branches) exercised by tests.",
    "Severity": "How much a defect impacts the system.",
    "Priority": "How urgently a defect should be fixed.",
    "Shift-left": "Moving testing activities earlier in the development lifecycle.",
    "Test double": "A stand-in (mock, stub, fake, spy) for a real dependency during tests.",
    "Flaky test": "A test that passes and fails intermittently without code changes.",
    "UAT": "User Acceptance Testing — validation by end users or the business.",
    "Exploratory testing": "Simultaneous learning, test design and execution, guided by charters.",
    "Traceability matrix": "A table linking requirements to the tests that cover them.",
}

QUIZ = [
    {
        "q": "Which statement reflects a core testing principle?",
        "options": [
            "Testing can prove software has no defects",
            "Testing shows the presence of defects, not their absence",
            "Exhaustive testing is achievable with automation",
            "Defects are spread evenly across all modules",
        ],
        "answer": 1,
        "why": "Testing reduces the probability of undiscovered defects but can never prove there are none.",
    },
    {
        "q": "An input field accepts ages 18–65. Which values best apply boundary value analysis?",
        "options": ["20, 40, 60", "17, 18, 65, 66", "0, 100", "18 only"],
        "answer": 1,
        "why": "Test just below, at, and just above each boundary: 17/18 and 65/66.",
    },
    {
        "q": "A typo on the About page that the CEO wants fixed before a demo tomorrow is…",
        "options": ["High severity, high priority", "Low severity, high priority",
                    "High severity, low priority", "Low severity, low priority"],
        "answer": 1,
        "why": "Minimal impact on functionality (low severity) but urgent for the business (high priority).",
    },
    {
        "q": "Which test level verifies interactions between modules?",
        "options": ["Unit", "Integration", "System", "Acceptance"],
        "answer": 1,
        "why": "Integration testing focuses on interfaces and interactions between components.",
    },
    {
        "q": "Reviewing a requirements document for ambiguity is an example of…",
        "options": ["Dynamic testing", "Static testing", "Regression testing", "Load testing"],
        "answer": 1,
        "why": "Static testing examines work products without executing code.",
    },
    {
        "q": "According to the test pyramid, which tests should you have the MOST of?",
        "options": ["End-to-end UI tests", "Manual tests", "Unit tests", "Exploratory sessions"],
        "answer": 2,
        "why": "Unit tests are fast, cheap and stable, so they form the wide base of the pyramid.",
    },
    {
        "q": "Running the same old tests repeatedly finds fewer new bugs over time. This is the…",
        "options": ["Defect clustering effect", "Pesticide paradox",
                    "Absence-of-errors fallacy", "Shift-left principle"],
        "answer": 1,
        "why": "Like pests becoming immune, defects stop being found by unchanged tests — review and refresh them.",
    },
    {
        "q": "After a developer fixes a bug, re-running the failed test to verify the fix is…",
        "options": ["Regression testing", "Confirmation testing", "Smoke testing", "Alpha testing"],
        "answer": 1,
        "why": "Confirmation (re-)testing checks the specific fix; regression testing checks for side effects.",
    },
    {
        "q": "Which is a non-functional test type?",
        "options": ["Login with valid credentials", "Checkout calculates tax",
                    "Page loads in under 2s with 1,000 users", "Password reset sends email"],
        "answer": 2,
        "why": "Performance is a non-functional characteristic — it's about *how well*, not *what*.",
    },
    {
        "q": "The most essential part of a bug report is…",
        "options": ["The tester's opinion of the developer", "Clear steps to reproduce",
                    "A long description of the whole app", "The test plan ID"],
        "answer": 1,
        "why": "If a developer can't reproduce it, they can't reliably fix it.",
    },
]

# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

LEVEL_BADGE = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}
TYPE_ICON = {
    "Course": "🎓", "Article": "📄", "Reference": "📘",
    "Video/Community": "👥", "Tool docs": "🛠️",
}


def render_source(src: dict) -> None:
    st.markdown(
        f"{TYPE_ICON.get(src['type'], '🔗')} **[{src['title']}]({src['url']})**  \n"
        f"<span style='opacity:0.75'>{src['provider']} · {src['type']} · "
        f"{LEVEL_BADGE[src['level']]} {src['level']}</span>  \n"
        f"{src['note']}",
        unsafe_allow_html=True,
    )


def sources_for(topic: str) -> list[dict]:
    return [s for s in SOURCES if topic in s["topics"]]


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

st.sidebar.title("🧪 QA Fundamentals")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home", "📚 Learn by topic", "🔗 Source library", "📖 Glossary", "✅ Quiz"],
)
st.sidebar.divider()
st.sidebar.caption(
    f"{len(TOPICS)} topics · {len(SOURCES)} free sources · {len(QUIZ)} quiz questions"
)
st.sidebar.caption("All linked resources are free to access (some ask for a free sign-up).")

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

if page == "🏠 Home":
    st.title("Quality Assurance Testing Fundamentals")
    st.write(
        "A free study hub for anyone starting out in software testing. Learn the core "
        "concepts, then go deeper with hand-picked free sources from ISTQB, Martin Fowler, "
        "Google, OWASP, Ministry of Testing and more."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Topics", len(TOPICS))
    c2.metric("Free sources", len(SOURCES))
    c3.metric("Quiz questions", len(QUIZ))

    st.subheader("Suggested learning path")
    path = [
        ("1. Learn the vocabulary", "Skim the Glossary and the 'What is testing' topic."),
        ("2. Study the foundations", "Read the ISTQB CTFL syllabus chapters 1–2."),
        ("3. Master test design", "Practice equivalence partitioning and boundary values."),
        ("4. Write tests & bug reports", "Draft test cases and bug reports for an app you use daily."),
        ("5. Explore", "Run a 30-minute exploratory session with the Test Heuristics Cheat Sheet."),
        ("6. Automate", "Take a beginner Test Automation University course."),
        ("7. Check yourself", "Take the quiz here, then the official ISTQB sample exam."),
    ]
    for step, detail in path:
        st.markdown(f"**{step}** — {detail}")

    st.subheader("Start here")
    for title in [
        "ISTQB Certified Tester Foundation Level (CTFL v4.0) syllabus",
        "The Practical Test Pyramid",
        "Test Automation University",
    ]:
        render_source(next(s for s in SOURCES if s["title"] == title))

elif page == "📚 Learn by topic":
    st.title("Learn by topic")
    topic = st.selectbox("Choose a topic", list(TOPICS.keys()))
    data = TOPICS[topic]

    st.subheader(topic)
    st.write(data["summary"])

    st.markdown("**Key points**")
    for point in data["key_points"]:
        st.markdown(f"- {point}")

    related = sources_for(topic)
    st.markdown(f"**Sources for this topic ({len(related)})**")
    if related:
        for src in related:
            render_source(src)
            st.write("")
    else:
        st.info("No sources tagged yet — check the Source library.")

    if topic == "Test design techniques":
        st.divider()
        st.subheader("🛠️ Try it: boundary value generator")
        col1, col2 = st.columns(2)
        lo = col1.number_input("Minimum valid value", value=18, step=1)
        hi = col2.number_input("Maximum valid value", value=65, step=1)
        if lo >= hi:
            st.warning("Minimum must be less than maximum.")
        else:
            rows = [
                (lo - 1, "Invalid", "Just below minimum"),
                (lo, "Valid", "Minimum"),
                (lo + 1, "Valid", "Just above minimum"),
                ((lo + hi) // 2, "Valid", "Nominal (equivalence class)"),
                (hi - 1, "Valid", "Just below maximum"),
                (hi, "Valid", "Maximum"),
                (hi + 1, "Invalid", "Just above maximum"),
            ]
            st.dataframe(
                pd.DataFrame(rows, columns=["Test value", "Expected", "Why"]),
                hide_index=True,
                use_container_width=True,
            )

elif page == "🔗 Source library":
    st.title("Source library")
    st.caption("Filter and search every free resource in the hub.")

    c1, c2, c3 = st.columns([2, 1, 1])
    query = c1.text_input("Search", placeholder="e.g. pyramid, API, security")
    types = c2.multiselect("Type", sorted({s["type"] for s in SOURCES}))
    levels = c3.multiselect("Level", ["Beginner", "Intermediate", "Advanced"])
    topic_filter = st.multiselect("Topic", list(TOPICS.keys()))

    def matches(s: dict) -> bool:
        text = f"{s['title']} {s['provider']} {s['note']}".lower()
        return (
            (not query or query.lower() in text)
            and (not types or s["type"] in types)
            and (not levels or s["level"] in levels)
            and (not topic_filter or any(t in s["topics"] for t in topic_filter))
        )

    results = [s for s in SOURCES if matches(s)]
    st.write(f"**{len(results)}** of {len(SOURCES)} sources")

    view = st.radio("View", ["Cards", "Table"], horizontal=True, label_visibility="collapsed")
    if view == "Cards":
        for src in results:
            with st.container(border=True):
                render_source(src)
                st.caption("Topics: " + ", ".join(src["topics"]))
    else:
        df = pd.DataFrame(
            [{"Title": s["title"], "Provider": s["provider"], "Type": s["type"],
              "Level": s["level"], "Link": s["url"]} for s in results]
        )
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={"Link": st.column_config.LinkColumn("Link")},
        )
        st.download_button(
            "⬇️ Download as CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name="qa_testing_sources.csv",
            mime="text/csv",
        )

elif page == "📖 Glossary":
    st.title("Glossary")
    term_q = st.text_input("Search terms", placeholder="e.g. regression")
    for term, definition in sorted(GLOSSARY.items()):
        if not term_q or term_q.lower() in (term + definition).lower():
            st.markdown(f"**{term}** — {definition}")
    st.caption("For the full official glossary, see glossary.istqb.org.")

elif page == "✅ Quiz":
    st.title("Check your understanding")

    if "quiz_order" not in st.session_state:
        st.session_state.quiz_order = random.sample(range(len(QUIZ)), len(QUIZ))
        st.session_state.submitted = False

    with st.form("quiz"):
        answers = {}
        for n, idx in enumerate(st.session_state.quiz_order, start=1):
            item = QUIZ[idx]
            answers[idx] = st.radio(
                f"**Q{n}.** {item['q']}",
                options=range(len(item["options"])),
                format_func=lambda i, item=item: item["options"][i],
                index=None,
                key=f"q_{idx}",
            )
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        score = sum(1 for idx, a in answers.items() if a == QUIZ[idx]["answer"])
        pct = score / len(QUIZ)
        st.subheader(f"Score: {score}/{len(QUIZ)}")
        st.progress(pct)
        if pct >= 0.8:
            st.success("Great work — you've got the fundamentals down.")
        elif pct >= 0.5:
            st.info("Solid start. Review the topics you missed below.")
        else:
            st.warning("Keep going — revisit 'Learn by topic' and try again.")

        for n, idx in enumerate(st.session_state.quiz_order, start=1):
            item = QUIZ[idx]
            ok = answers[idx] == item["answer"]
            with st.expander(f"{'✅' if ok else '❌'} Q{n}. {item['q']}"):
                st.markdown(f"**Correct answer:** {item['options'][item['answer']]}")
                st.markdown(item["why"])

    if st.button("🔄 Shuffle & restart"):
        for key in list(st.session_state.keys()):
            if key.startswith("q_") or key == "quiz_order":
                del st.session_state[key]
        st.rerun()

st.sidebar.divider()
st.sidebar.caption("Built with Streamlit · Free to use and share")
