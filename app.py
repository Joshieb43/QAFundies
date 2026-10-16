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

# Practice quizzes, one per chapter of the ISTQB CTFL v4.0.1 syllabus.
# Questions are original practice questions (not official exam questions).
# "answer" is the index of the correct option; options are shuffled at runtime.
# "ref" is the syllabus section the question is based on.
QUIZZES = {
    "ch1": {
        "tab": "Ch 1 · Fundamentals",
        "title": "Chapter 1 — Fundamentals of Testing",
        "questions": [
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
                "ref": "1.3",
            },
            {
                "q": "Running the same old tests repeatedly finds fewer new bugs over time. Which principle is this?",
                "options": ["Defects cluster together", "Tests wear out",
                            "Absence-of-defects fallacy", "Early testing saves time and money"],
                "answer": 1,
                "why": "Repeated tests become less effective at finding new defects (formerly called the "
                       "'pesticide paradox'). Update tests and test data, and add new tests.",
                "ref": "1.3",
            },
            {
                "q": "A team tests every specified requirement and fixes every defect found, but users reject "
                     "the system because it doesn't fit how they work. This illustrates…",
                "options": ["Exhaustive testing is impossible", "The absence-of-defects fallacy",
                            "Defects cluster together", "Testing is context dependent"],
                "answer": 1,
                "why": "Verification alone doesn't guarantee success; validation against users' needs is also needed.",
                "ref": "1.3",
            },
            {
                "q": "A test triggers a failure. Which activity finds, analyzes and removes the defect that caused it?",
                "options": ["Confirmation testing", "Debugging", "Regression testing", "Test analysis"],
                "answer": 1,
                "why": "Testing and debugging are separate. Debugging reproduces the failure, diagnoses the "
                       "defect and fixes it; confirmation testing then checks the fix.",
                "ref": "1.1.2",
            },
            {
                "q": "A developer misreads a requirement and writes code that calculates tax incorrectly, so a "
                     "customer is charged the wrong amount. Which mapping is correct?",
                "options": [
                    "Misreading = error, wrong code = defect, wrong charge = failure",
                    "Misreading = defect, wrong code = failure, wrong charge = error",
                    "Misreading = failure, wrong code = error, wrong charge = defect",
                    "Misreading = failure, wrong code = defect, wrong charge = error",
                ],
                "answer": 0,
                "why": "People make errors (mistakes), which produce defects (bugs), which may cause failures when executed.",
                "ref": "1.2.3",
            },
            {
                "q": "Which statement best describes the difference between QA and testing?",
                "options": [
                    "QA is product-oriented and corrective; testing is process-oriented and preventive",
                    "QA is process-oriented and preventive; testing is product-oriented and corrective",
                    "QA and testing are two names for the same thing",
                    "QA is the responsibility of the test team only",
                ],
                "answer": 1,
                "why": "QA improves processes to prevent defects and is everyone's responsibility; testing is a "
                       "form of quality control on the product.",
                "ref": "1.2.2",
            },
            {
                "q": "Which test activity answers the question \"how to test?\" by turning test conditions into test cases?",
                "options": ["Test analysis", "Test design", "Test implementation", "Test execution"],
                "answer": 1,
                "why": "Test analysis decides what to test; test design elaborates test conditions into test "
                       "cases and other testware.",
                "ref": "1.4.1",
            },
            {
                "q": "Which work product is created during test completion?",
                "options": ["Test charter", "Test execution schedule", "Test completion report", "Coverage items"],
                "answer": 2,
                "why": "Test completion produces the test completion report, lessons learned, improvement "
                       "actions and change requests.",
                "ref": "1.4.3",
            },
            {
                "q": "Which arrangement gives the highest level of test independence?",
                "options": ["Developers testing their own code", "A peer from the same team",
                            "Testers from another team in the same organization",
                            "Testers from outside the organization"],
                "answer": 3,
                "why": "Independence rises from author → same-team peer → other team → outside the organization.",
                "ref": "1.5.3",
            },
        ],
    },
    "ch2": {
        "tab": "Ch 2 · SDLC",
        "title": "Chapter 2 — Testing Throughout the Software Development Lifecycle",
        "questions": [
            {
                "q": "Which test level focuses on the interfaces and interactions between components?",
                "options": ["Component testing", "Component integration testing", "System testing",
                            "Acceptance testing"],
                "answer": 1,
                "why": "Component integration testing targets interfaces between components and depends on the "
                       "integration strategy (bottom-up, top-down, big-bang).",
                "ref": "2.2.1",
            },
            {
                "q": "Which test level focuses mainly on validation and on showing the system is ready for deployment?",
                "options": ["Component testing", "Component integration testing", "System testing",
                            "Acceptance testing"],
                "answer": 3,
                "why": "Acceptance testing (UAT, operational, contractual, regulatory, alpha, beta) shows the "
                       "system meets the users' business needs.",
                "ref": "2.2.1",
            },
            {
                "q": "After a developer fixes a bug, re-running the failed test to verify the fix is…",
                "options": ["Regression testing", "Confirmation testing", "Smoke testing", "Alpha testing"],
                "answer": 1,
                "why": "Confirmation testing checks the specific fix; regression testing checks for side effects.",
                "ref": "2.2.3",
            },
            {
                "q": "Which is a non-functional test?",
                "options": ["Login with valid credentials", "Checkout calculates tax",
                            "Page loads in under 2s with 1,000 users", "Password reset sends an email"],
                "answer": 2,
                "why": "Performance efficiency is a non-functional characteristic: it's about how well, not what.",
                "ref": "2.2.2",
            },
            {
                "q": "Which test-first approach describes desired behavior in simple natural language, usually "
                     "in Given/When/Then format?",
                "options": ["Test-driven development (TDD)", "Acceptance test-driven development (ATDD)",
                            "Behavior-driven development (BDD)", "Domain-driven design (DDD)"],
                "answer": 2,
                "why": "BDD expresses behavior as readable scenarios that can be turned into executable tests.",
                "ref": "2.1.3",
            },
            {
                "q": "Which is an example of shift left?",
                "options": [
                    "Running performance tests only once the full system is in a production-like environment",
                    "Reviewing the requirements from a tester's perspective before any code is written",
                    "Adding more testers in the final week before release",
                    "Postponing static analysis until after system testing",
                ],
                "answer": 1,
                "why": "Shift left means testing earlier, e.g., reviewing specifications, writing tests before "
                       "code, CI and early static analysis.",
                "ref": "2.1.5",
            },
            {
                "q": "Which is a benefit of DevOps for testing?",
                "options": [
                    "Manual testing is no longer needed",
                    "Fast feedback on code quality and on whether changes break existing code",
                    "Test automation needs no maintenance",
                    "Non-functional characteristics become less visible",
                ],
                "answer": 1,
                "why": "DevOps pipelines give fast feedback and reduce regression risk, but manual testing from "
                       "the user's perspective is still needed.",
                "ref": "2.1.4",
            },
            {
                "q": "What is advisable before deciding how much regression testing a change needs?",
                "options": ["Impact analysis", "Exploratory testing", "A retrospective", "Three-point estimation"],
                "answer": 0,
                "why": "Impact analysis shows which parts of the software could be affected by the change.",
                "ref": "2.2.3",
            },
            {
                "q": "Which of these triggers maintenance testing?",
                "options": ["Writing user stories for a brand-new product",
                            "Migrating an operational system to a new platform",
                            "Holding a sprint planning meeting", "Creating the first test plan"],
                "answer": 1,
                "why": "Triggers include modifications (enhancements, hot fixes), upgrades or migrations of the "
                       "environment, and retirement.",
                "ref": "2.3",
            },
            {
                "q": "What do participants discuss in a retrospective?",
                "options": [
                    "Only the defects found by testers",
                    "What went well, what could improve, and how to keep the successes and apply the improvements",
                    "Individual performance ratings of team members",
                    "Effort estimates for the next release",
                ],
                "answer": 1,
                "why": "Retrospectives drive continuous improvement; results are usually recorded in the test "
                       "completion report.",
                "ref": "2.1.6",
            },
        ],
    },
    "ch3": {
        "tab": "Ch 3 · Static testing",
        "title": "Chapter 3 — Static Testing",
        "questions": [
            {
                "q": "Reviewing a requirements document for ambiguity is an example of…",
                "options": ["Dynamic testing", "Static testing", "Regression testing", "Load testing"],
                "answer": 1,
                "why": "Static testing examines work products without executing code.",
                "ref": "3.1",
            },
            {
                "q": "Which defect is typically easier to find with static testing than with dynamic testing?",
                "options": ["A memory leak that appears after hours of heavy use", "Unreachable code",
                            "Slow responses with 1,000 concurrent users", "A crash in one specific browser"],
                "answer": 1,
                "why": "Static testing finds defects directly, including ones dynamic testing can't reach, such "
                       "as unreachable code.",
                "ref": "3.1.3",
            },
            {
                "q": "Which review role makes sure review meetings run effectively, including mediation and "
                     "time management?",
                "options": ["Author", "Scribe", "Moderator (facilitator)", "Manager"],
                "answer": 2,
                "why": "The moderator runs the meeting and keeps a safe environment where everyone can speak freely.",
                "ref": "3.2.3",
            },
            {
                "q": "Who records the anomalies, decisions and new findings during a review meeting?",
                "options": ["Reviewer", "Scribe (recorder)", "Review leader", "Author"],
                "answer": 1,
                "why": "The scribe collates anomalies from reviewers and records review information.",
                "ref": "3.2.3",
            },
            {
                "q": "Which review type is the most formal, follows the complete review process and aims to "
                     "find the maximum number of anomalies?",
                "options": ["Informal review", "Walkthrough", "Technical review", "Inspection"],
                "answer": 3,
                "why": "Inspections are the most formal review type; metrics are collected, and the author "
                       "can't be the review leader or scribe.",
                "ref": "3.2.4",
            },
            {
                "q": "Which review type is led by the author of the work product?",
                "options": ["Inspection", "Technical review", "Walkthrough", "Audit"],
                "answer": 2,
                "why": "A walkthrough is led by the author and can educate reviewers, build consensus and find anomalies.",
                "ref": "3.2.4",
            },
            {
                "q": "In which review activity are anomalies discussed and a decision made on each one's "
                     "status, owner and required actions?",
                "options": ["Planning", "Individual review", "Communication and analysis", "Fixing and reporting"],
                "answer": 2,
                "why": "Anomalies aren't necessarily defects, so they're analyzed and discussed, usually in a review meeting.",
                "ref": "3.2.2",
            },
            {
                "q": "Which is a success factor for reviews?",
                "options": [
                    "Using reviews to evaluate participants' performance",
                    "Reviewing very large documents in a single session",
                    "Defining clear objectives and measurable exit criteria",
                    "Skipping preparation time to keep momentum",
                ],
                "answer": 2,
                "why": "Clear objectives, small chunks, enough preparation time and management support all help. "
                       "Evaluating participants should never be an objective.",
                "ref": "3.2.5",
            },
        ],
    },
    "ch4": {
        "tab": "Ch 4 · Test design",
        "title": "Chapter 4 — Test Analysis and Design",
        "questions": [
            {
                "q": "An input field accepts ages 18–65. Which values does 2-value boundary value analysis give?",
                "options": ["20, 40, 60", "17, 18, 65, 66", "0, 100", "18 only"],
                "answer": 1,
                "why": "2-value BVA tests each boundary and its closest neighbor in the adjacent partition: 17/18 and 65/66.",
                "ref": "4.2.2",
            },
            {
                "q": "A field accepts integers 1–100. Using 3-value BVA, which values cover the lower boundary?",
                "options": ["0 and 1", "0, 1 and 2", "1, 2 and 3", "1, 50 and 100"],
                "answer": 1,
                "why": "3-value BVA tests the boundary value and both its neighbors, so it's more rigorous than 2-value BVA.",
                "ref": "4.2.2",
            },
            {
                "q": "A field accepts integers 1–10; values below 1 or above 10 are rejected. What is the minimum "
                     "number of test cases for 100% equivalence partition coverage?",
                "options": ["1", "2", "3", "6"],
                "answer": 2,
                "why": "There are three partitions (below 1, 1–10, above 10); 100% coverage exercises each one, "
                       "including invalid partitions.",
                "ref": "4.2.1",
            },
            {
                "q": "A business rule depends on 3 independent true/false conditions, and every combination is "
                     "feasible. How many columns does the full decision table have?",
                "options": ["3", "6", "8", "9"],
                "answer": 2,
                "why": "A full table covers every combination: 2³ = 8 rules (columns).",
                "ref": "4.2.3",
            },
            {
                "q": "Which state transition coverage criterion requires exercising all valid transitions AND "
                     "attempting invalid ones?",
                "options": ["All states coverage", "Valid transitions (0-switch) coverage",
                            "All transitions coverage", "Branch coverage"],
                "answer": 2,
                "why": "All transitions coverage includes invalid transitions from the state table and is the "
                       "minimum for mission- and safety-critical software.",
                "ref": "4.2.4",
            },
            {
                "q": "Which statement about white-box coverage is true?",
                "options": [
                    "100% statement coverage guarantees 100% branch coverage",
                    "100% branch coverage guarantees 100% statement coverage",
                    "Statement and branch coverage are always equal",
                    "Neither can be measured objectively",
                ],
                "answer": 1,
                "why": "Branch coverage subsumes statement coverage, but not the other way round.",
                "ref": "4.3.2",
            },
            {
                "q": "Code: `if (x > 0) { y = 1 }` with no else. What is the minimum number of tests for 100% "
                     "statement coverage, and for 100% branch coverage?",
                "options": ["1 and 1", "1 and 2", "2 and 2", "2 and 1"],
                "answer": 1,
                "why": "One test with x > 0 runs every statement; branch coverage also needs the false outcome (x ≤ 0).",
                "ref": "4.3",
            },
            {
                "q": "A key weakness of white-box testing is that it may not detect…",
                "options": ["defects in rarely executed code", "requirements the code never implemented",
                            "defects in decision logic", "unreachable code"],
                "answer": 1,
                "why": "White-box tests are derived from the code, so defects of omission (missing features) can be missed.",
                "ref": "4.3.3",
            },
            {
                "q": "Session-based exploratory testing is done within a time box and guided by a…",
                "options": ["Test charter", "Decision table", "Traceability matrix", "Test execution schedule"],
                "answer": 0,
                "why": "The charter holds the test objectives; a debriefing usually follows the session.",
                "ref": "4.4.2",
            },
            {
                "q": "A tester lists likely mistakes (empty inputs, wrong date formats, missing parameters) from "
                     "past failures and designs tests to expose them. Which technique is this?",
                "options": ["Error guessing (fault attack)", "Decision table testing", "Statement testing",
                            "Equivalence partitioning"],
                "answer": 0,
                "why": "Error guessing anticipates errors, defects and failures from experience; fault attacks "
                       "are one way to do it.",
                "ref": "4.4.1",
            },
            {
                "q": "In the INVEST criteria for good user stories, what does the \"T\" stand for?",
                "options": ["Traceable", "Testable", "Timely", "Technical"],
                "answer": 1,
                "why": "Independent, Negotiable, Valuable, Estimable, Small, Testable.",
                "ref": "4.5.1",
            },
            {
                "q": "In the \"3 C's\" of a user story, what is the \"Confirmation\"?",
                "options": ["The index card or board entry", "The acceptance criteria",
                            "Sign-off from the project manager", "The conversation about how it's used"],
                "answer": 1,
                "why": "Card, Conversation, Confirmation, where Confirmation is the acceptance criteria.",
                "ref": "4.5.1",
            },
            {
                "q": "In ATDD, after writing the positive test cases, what does the team typically cover next?",
                "options": ["Negative tests, then non-functional characteristics", "Unit tests only",
                            "Nothing more; positive tests are enough", "Code coverage targets"],
                "answer": 0,
                "why": "Start with positive cases, then negative testing, then non-functional quality characteristics.",
                "ref": "4.5.3",
            },
        ],
    },
    "ch5": {
        "tab": "Ch 5 · Managing",
        "title": "Chapter 5 — Managing the Test Activities",
        "questions": [
            {
                "q": "A typo on the About page that the CEO wants fixed before a demo tomorrow is…",
                "options": ["High severity, high priority", "Low severity, high priority",
                            "High severity, low priority", "Low severity, low priority"],
                "answer": 1,
                "why": "Severity is the impact (low here); priority is the urgency to fix (high for the business).",
                "ref": "5.5",
            },
            {
                "q": "According to the test pyramid, which tests should you have the MOST of?",
                "options": ["End-to-end UI tests", "Manual tests", "Unit (component) tests", "Exploratory sessions"],
                "answer": 2,
                "why": "Bottom-layer tests are small, isolated and fast, so you need many of them; end-to-end tests are few.",
                "ref": "5.1.6",
            },
            {
                "q": "Which part of a defect report matters most for getting the defect fixed?",
                "options": ["The tester's opinion of the developer", "A description that lets others reproduce the failure",
                            "A long description of the whole application", "The test plan ID"],
                "answer": 1,
                "why": "Reports should include the steps, logs and screenshots needed to reproduce and resolve the anomaly.",
                "ref": "5.5",
            },
            {
                "q": "Three-point estimation gives a = 4, m = 7, b = 16 person-days. Using E = (a + 4m + b) / 6 "
                     "and SD = (b − a) / 6, what is the estimate?",
                "options": ["7 person-days", "8 ± 2 person-days", "9 ± 2 person-days", "8 ± 4 person-days"],
                "answer": 1,
                "why": "E = (4 + 28 + 16) / 6 = 8 and SD = (16 − 4) / 6 = 2.",
                "ref": "5.1.4",
            },
            {
                "q": "Past projects had a development-to-test effort ratio of 5:2. The new project needs 500 "
                     "person-days of development. What is the estimated test effort?",
                "options": ["100 person-days", "200 person-days", "250 person-days", "1,250 person-days"],
                "answer": 1,
                "why": "Estimation based on ratios: 500 × 2/5 = 200 person-days.",
                "ref": "5.1.4",
            },
            {
                "q": "Which of these is a product risk?",
                "options": ["A key tester leaves the project", "A supplier delivers a component late",
                            "The system responds too slowly for users", "The test budget is cut"],
                "answer": 2,
                "why": "Product risks concern quality characteristics; the others are project risks "
                       "(people, supplier, organizational).",
                "ref": "5.2.2",
            },
            {
                "q": "Which two factors determine a risk's level?",
                "options": ["Likelihood and impact", "Severity and priority",
                            "Number of test cases and number of defects", "Cost and schedule"],
                "answer": 0,
                "why": "Risk level combines risk likelihood with risk impact (harm).",
                "ref": "5.2.1",
            },
            {
                "q": "Which testing quadrant contains exploratory testing, usability testing and user acceptance testing?",
                "options": ["Q1: technology facing, supports the team", "Q2: business facing, supports the team",
                            "Q3: business facing, critiques the product", "Q4: technology facing, critiques the product"],
                "answer": 2,
                "why": "Q3 tests are user-oriented and often manual.",
                "ref": "5.1.7",
            },
            {
                "q": "In Agile development, the exit criteria for a releasable item are often called the…",
                "options": ["Definition of Ready", "Definition of Done", "Acceptance criteria", "Test charter"],
                "answer": 1,
                "why": "Definition of Done = exit criteria; Definition of Ready = entry criteria for a user story.",
                "ref": "5.1.3",
            },
            {
                "q": "Which is an example of test control?",
                "options": [
                    "Counting how many tests passed and failed",
                    "Reprioritizing tests when an identified risk becomes an issue",
                    "Archiving testware at the end of the project",
                    "Writing the test completion report",
                ],
                "answer": 1,
                "why": "Monitoring gathers information; control uses it to take corrective actions (control directives).",
                "ref": "5.3",
            },
            {
                "q": "A high-priority test case depends on a lower-priority test case. What should happen?",
                "options": ["Skip the lower-priority test", "Run the lower-priority test first",
                            "Run the high-priority test first anyway", "Delete the dependency from the plan"],
                "answer": 1,
                "why": "Dependencies override pure priority order: the prerequisite must run first.",
                "ref": "5.1.5",
            },
            {
                "q": "Being able to revert to a previous baseline to reproduce earlier test results is a benefit of…",
                "options": ["Configuration management", "Risk management", "Defect management", "Test estimation"],
                "answer": 0,
                "why": "Configuration management uniquely identifies, versions and tracks testware and test items.",
                "ref": "5.4",
            },
        ],
    },
    "ch6": {
        "tab": "Ch 6 · Tools",
        "title": "Chapter 6 — Test Tools",
        "questions": [
            {
                "q": "Which is a potential benefit of test automation?",
                "options": ["It removes the need for human critical thinking",
                            "Shorter test execution times and faster feedback",
                            "Test scripts never need maintenance",
                            "Buying the tool guarantees success"],
                "answer": 1,
                "why": "Automation saves repetitive work and speeds feedback, but tools still need effort to "
                       "introduce and maintain.",
                "ref": "6.2",
            },
            {
                "q": "Which is a risk of test automation?",
                "options": ["More objective coverage measurement", "Unrealistic expectations about what the tool can do",
                            "Greater consistency and repeatability", "More time for testers to design new tests"],
                "answer": 1,
                "why": "The other three are benefits. Risks include unrealistic expectations, bad estimates and "
                       "over-reliance on the tool.",
                "ref": "6.2",
            },
            {
                "q": "Which type of tool supports reviews and static analysis?",
                "options": ["Test management tools", "Static testing tools", "Non-functional testing tools",
                            "Collaboration tools"],
                "answer": 1,
                "why": "Static testing tools support reviews and static analysis.",
                "ref": "6.1",
            },
            {
                "q": "Simulating thousands of concurrent users for a load test needs which type of tool?",
                "options": ["DevOps tool", "Collaboration tool", "Non-functional testing tool", "Test design tool"],
                "answer": 2,
                "why": "Non-functional testing tools enable tests that are difficult or impossible to do manually.",
                "ref": "6.1",
            },
            {
                "q": "Why can depending on an open-source test tool be a risk?",
                "options": ["Open-source tools can't run automated tests",
                            "The project may be abandoned and stop getting updates",
                            "They never work with CI pipelines", "They can't be version controlled"],
                "answer": 1,
                "why": "Abandoned projects, or components needing frequent updates, are listed automation risks.",
                "ref": "6.2",
            },
            {
                "q": "Can a spreadsheet count as a test tool?",
                "options": ["No, only commercial testing tools count",
                            "Yes, any tool that assists in testing counts",
                            "Only if it runs automated tests", "Only when used for defect tracking"],
                "answer": 1,
                "why": "The syllabus explicitly includes any tool that assists testing, e.g., a spreadsheet.",
                "ref": "6.1",
            },
        ],
    },
}

MIXED_QUIZ_SIZE = 10
QUESTION_COUNT = sum(len(quiz["questions"]) for quiz in QUIZZES.values())

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
        f"{LEVEL_BADGE.get(src['level'], '⚪')} {src['level']}</span>  \n"
        f"{src['note']}",
        unsafe_allow_html=True,
    )


def sources_for(topic: str) -> list[dict]:
    return [s for s in SOURCES if topic in s["topics"]]


def quiz_question(ref: tuple[str, int]) -> dict:
    quiz_key, idx = ref
    return QUIZZES[quiz_key]["questions"][idx]


def new_quiz_state(quiz_key: str) -> dict:
    """Pick and shuffle the questions (and each question's options) for one quiz."""
    if quiz_key == "mixed":
        pool = [(k, i) for k, quiz in QUIZZES.items() for i in range(len(quiz["questions"]))]
        refs = random.sample(pool, MIXED_QUIZ_SIZE)
    else:
        count = len(QUIZZES[quiz_key]["questions"])
        refs = random.sample([(quiz_key, i) for i in range(count)], count)
    options = {}
    for ref in refs:
        count = len(quiz_question(ref)["options"])
        options[ref] = random.sample(range(count), count)
    return {"refs": refs, "options": options, "results": None}


def render_quiz(quiz_key: str, heading: str) -> None:
    state_key = f"quiz_{quiz_key}"
    if state_key not in st.session_state:
        st.session_state[state_key] = new_quiz_state(quiz_key)
    state = st.session_state[state_key]
    refs = state["refs"]

    st.subheader(heading)
    with st.form(f"form_{quiz_key}"):
        answers = {}
        for n, ref in enumerate(refs, start=1):
            item = quiz_question(ref)
            answers[ref] = st.radio(
                f"**Q{n}.** {item['q']}",
                options=state["options"][ref],
                format_func=lambda i, item=item: item["options"][i],
                index=None,
                key=f"{quiz_key}_q_{ref[0]}_{ref[1]}",
            )
        submitted = st.form_submit_button("Submit answers")

    if submitted:
        unanswered = [n for n, ref in enumerate(refs, start=1) if answers[ref] is None]
        if unanswered:
            state["results"] = None
            st.warning(
                "Please answer every question before submitting. Unanswered: "
                + ", ".join(f"Q{n}" for n in unanswered)
            )
        else:
            state["results"] = answers

    # Results live in session state so they survive reruns triggered from other tabs.
    results = state["results"]
    if results:
        score = sum(1 for ref, a in results.items() if a == quiz_question(ref)["answer"])
        pct = score / len(refs)
        st.markdown(f"#### Score: {score}/{len(refs)}")
        st.progress(pct)
        if pct >= 0.8:
            st.success("Great work — you've got this material down.")
        elif pct >= 0.5:
            st.info("Solid start. Review the questions you missed below.")
        else:
            st.warning("Keep going — revisit the syllabus sections below and try again.")

        for n, ref in enumerate(refs, start=1):
            item = quiz_question(ref)
            ok = results[ref] == item["answer"]
            with st.expander(f"{'✅' if ok else '❌'} Q{n}. {item['q']}"):
                if not ok:
                    st.markdown(f"**Your answer:** {item['options'][results[ref]]}")
                st.markdown(f"**Correct answer:** {item['options'][item['answer']]}")
                st.markdown(item["why"])
                st.caption(f"CTFL v4.0.1 syllabus, section {item['ref']}")

    if st.button("🔄 Shuffle & restart", key=f"restart_{quiz_key}"):
        for key in list(st.session_state.keys()):
            if key.startswith(f"{quiz_key}_q_"):
                del st.session_state[key]
        del st.session_state[state_key]
        st.rerun()


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
    f"{len(TOPICS)} topics · {len(SOURCES)} free sources · "
    f"{len(QUIZZES)} chapter quizzes ({QUESTION_COUNT} questions)"
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
    c3.metric("Quiz questions", QUESTION_COUNT)

    st.subheader("Suggested learning path")
    path = [
        ("1. Learn the vocabulary", "Skim the Glossary and the 'What is testing' topic."),
        ("2. Study the foundations", "Read the ISTQB CTFL syllabus chapters 1–2."),
        ("3. Master test design", "Practice equivalence partitioning and boundary values."),
        ("4. Write tests & bug reports", "Draft test cases and bug reports for an app you use daily."),
        ("5. Explore", "Run a 30-minute exploratory session with the Test Heuristics Cheat Sheet."),
        ("6. Automate", "Take a beginner Test Automation University course."),
        ("7. Check yourself", "Take the chapter quizzes here, then the official ISTQB sample exam."),
    ]
    for step, detail in path:
        st.markdown(f"**{step}** — {detail}")

    st.subheader("Start here")
    for title in [
        "ISTQB Certified Tester Foundation Level (CTFL v4.0) syllabus",
        "The Practical Test Pyramid",
        "Test Automation University",
    ]:
        src = next((s for s in SOURCES if s["title"] == title), None)
        if src:
            render_source(src)

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
            # Boundaries come first so they keep their label when a narrow range
            # makes the inner values (min+1, max-1, nominal) collide with them.
            candidates = [
                (lo - 1, "Invalid", "Just below minimum"),
                (lo, "Valid", "Minimum"),
                (hi, "Valid", "Maximum"),
                (hi + 1, "Invalid", "Just above maximum"),
                (lo + 1, "Valid", "Just above minimum"),
                (hi - 1, "Valid", "Just below maximum"),
                ((lo + hi) // 2, "Valid", "Nominal (equivalence class)"),
            ]
            rows = {}
            for value, expected, why in candidates:
                rows.setdefault(value, (value, expected, why))
            st.dataframe(
                pd.DataFrame(sorted(rows.values()), columns=["Test value", "Expected", "Why"]),
                hide_index=True,
                width="stretch",
            )
            st.caption(
                "This uses three-value boundary analysis: it adds min+1 and max−1 to the "
                "classic two-value set (min−1, min, max, max+1), plus one nominal value."
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
        text = f"{s['title']} {s['provider']} {s['note']} {' '.join(s['topics'])}".lower()
        return (
            (not query or query.lower() in text)
            and (not types or s["type"] in types)
            and (not levels or s["level"] in levels)
            and (not topic_filter or any(t in s["topics"] for t in topic_filter))
        )

    results = [s for s in SOURCES if matches(s)]
    st.write(f"**{len(results)}** of {len(SOURCES)} sources")

    view = st.radio("View", ["Cards", "Table"], horizontal=True, label_visibility="collapsed")
    if not results:
        st.info("No sources match these filters. Try a different search or clear a filter.")
    elif view == "Cards":
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
            width="stretch",
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
    shown = 0
    for term, definition in sorted(GLOSSARY.items()):
        if not term_q or term_q.lower() in f"{term} {definition}".lower():
            st.markdown(f"**{term}** — {definition}")
            shown += 1
    if not shown:
        st.info(f"No terms match '{term_q}'.")
    st.caption("For the full official glossary, see glossary.istqb.org.")

elif page == "✅ Quiz":
    st.title("Check your understanding")
    st.caption(
        "Practice quizzes for each chapter of the ISTQB CTFL v4.0.1 syllabus, plus a mixed review. "
        "These are original practice questions, not official exam questions."
    )
    tabs = st.tabs([quiz["tab"] for quiz in QUIZZES.values()] + ["🎲 Mixed review"])
    for tab, (quiz_key, quiz) in zip(tabs, QUIZZES.items()):
        with tab:
            render_quiz(quiz_key, quiz["title"])
    with tabs[-1]:
        render_quiz("mixed", f"Mixed review — {MIXED_QUIZ_SIZE} random questions from all chapters")

st.sidebar.divider()
st.sidebar.caption("Built with Streamlit · Free to use and share")
