import os
from io import BytesIO
import streamlit as st
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch

st.set_page_config(page_title="EduPath Pakistan", page_icon="🎓", layout="wide")

SYSTEM_PROMPT = """
You are EduPath Pakistan, an AI-powered education and career counselor
designed specifically for students in Pakistan.

Help students understand realistic education, career and skills pathways.
You may communicate in English, Urdu, or Roman Urdu.

Rules:
1. Never guarantee admission, employment, or scholarships.
2. Never invent current university requirements, fees, deadlines,
   scholarships, or eligibility criteria.
3. Tell students to verify current information with official sources.
4. University is not the only pathway. Consider public/private universities,
   technical/vocational education, DAE, certifications, online learning,
   skills, internships, freelancing and entrepreneurship.
5. Do not discourage students because of low marks.
6. Focus on: "WHAT SHOULD THIS STUDENT DO NEXT?"
7. Consider education, marks, subjects, city, career goal, budget and gap year.
8. Keep language simple, practical and constructive.
"""

def get_client():
    key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY"))
    return Groq(api_key=key) if key else None

def build_profile(p):
    return f"""
STUDENT PROFILE
Name: {p.get('name') or 'Not provided'}
Education: {p.get('education') or 'Not provided'}
Marks / Percentage: {p.get('marks') or 'Not provided'}
Major Subjects: {p.get('subjects') or 'Not provided'}
City: {p.get('city') or 'Not provided'}
Desired Career / Field: {p.get('career_goal') or 'Not provided'}
Education Budget: {p.get('budget') or 'Not provided'}
Considering Gap Year: {p.get('gap_year') or 'Not provided'}
"""

def call_groq(messages, max_tokens=2000, temperature=0.4):
    client = get_client()
    if not client:
        raise RuntimeError("GROQ_API_KEY is not configured in Streamlit Secrets.")
    model = st.secrets.get("GROQ_MODEL", "openai/gpt-oss-120b")
    response = client.chat.completions.create(
        model=model, messages=messages,
        temperature=temperature, max_tokens=max_tokens
    )
    return response.choices[0].message.content

def generate_report(profile):
    prompt = f"""
Create a personalized education and career guidance report for this Pakistani student.

{build_profile(profile)}

Use this structure:
# 🎓 EduPath Pakistan — Personalized Education Report
## 1. Student Profile
## 2. Situation Analysis
## 3. Recommended Primary Pathway
## 4. Alternative Pathways
## 5. Career Direction
## 6. Skills to Develop
## 7. University Strategy
## 8. Financial Strategy
## 9. 90-Day Action Plan
### Days 1–30 — Understand
### Days 31–60 — Prepare
### Days 61–90 — Act
## 10. Risks & Things to Verify
## 11. Immediate Next Steps
## 12. Encouragement

Be realistic. Do not invent current university facts, fees, deadlines or
scholarships. Tell the student to verify current information with official
sources. Do not guarantee admission or employment.
"""
    return call_groq([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ], 4000, 0.3)

def counselor_reply(profile, history, message):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": build_profile(profile)}
    ] + history + [{"role": "user", "content": message}]
    return call_groq(messages, 1800, 0.4)

def markdown_to_pdf(text):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4, rightMargin=.65*inch, leftMargin=.65*inch,
        topMargin=.65*inch, bottomMargin=.65*inch
    )
    styles = getSampleStyleSheet()
    title = ParagraphStyle("ReportTitle", parent=styles["Title"],
                           alignment=TA_CENTER, fontSize=18, leading=22, spaceAfter=16)
    heading = ParagraphStyle("ReportHeading", parent=styles["Heading2"],
                             fontSize=13, leading=17, spaceBefore=10, spaceAfter=6)
    body = ParagraphStyle("ReportBody", parent=styles["BodyText"],
                          fontSize=9.5, leading=14, spaceAfter=6)
    story = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            story.append(Spacer(1, 5)); continue
        safe = line.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
        if line.startswith("# "): story.append(Paragraph(safe[2:], title))
        elif line.startswith("## "): story.append(Paragraph(safe[3:], heading))
        elif line.startswith("### "): story.append(Paragraph(safe[4:], heading))
        elif line.startswith("- "): story.append(Paragraph("• " + safe[2:], body))
        else: story.append(Paragraph(safe, body))
    doc.build(story)
    return buf.getvalue()

st.markdown("""
<style>
.hero{padding:30px;border-radius:20px;text-align:center;background:linear-gradient(135deg,#eff6ff,#f8fafc);border:1px solid #dbeafe;margin-bottom:25px}
.hero h1{font-size:40px;margin-bottom:8px}.hero p{font-size:17px}
.card{padding:18px;border-radius:15px;border:1px solid #e2e8f0}
</style>
""", unsafe_allow_html=True)


# ============================================================
# EDUPATH PAKISTAN — HERO UI + FONT COLOR FIX
# ============================================================

st.markdown("""
<style>

/* =========================================================
   HERO CONTAINER
   ========================================================= */

.hero {
    padding: 35px 25px;
    border-radius: 20px;
    text-align: center;

    /* Light background */
    background: linear-gradient(
        135deg,
        #eff6ff 0%,
        #f8fafc 50%,
        #e0ecff 100%
    );

    border: 1px solid #dbeafe;

    margin-top: 10px;
    margin-bottom: 30px;

    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}


/* =========================================================
   EDUPATH MAIN TITLE
   ========================================================= */

.hero h1 {
    font-size: 42px !important;

    /* BLUE FONT */
    color: #1d4ed8 !important;

    font-weight: 800 !important;

    margin-top: 0 !important;
    margin-bottom: 12px !important;

    line-height: 1.2 !important;
}


/* =========================================================
   HERO NORMAL PARAGRAPH
   ========================================================= */

.hero p {

    /* DARK GRAY FONT */
    color: #334155 !important;

    font-size: 17px !important;

    line-height: 1.6 !important;

    margin-top: 8px !important;
    margin-bottom: 8px !important;
}


/* =========================================================
   AI-POWERED SUBHEADING
   ========================================================= */

.hero p strong,
.hero p b {

    /* VERY DARK FONT */
    color: #0f172a !important;

    font-size: 19px !important;

    font-weight: 700 !important;
}


/* =========================================================
   STREAMLIT HEADINGS
   ========================================================= */

/*
Do not force Streamlit's normal headings to black.
This allows Student Profile, Generate Report,
AI Counselor etc. to remain readable in both
dark mode and light mode.
*/

h1, h2, h3 {
    font-weight: 700;
}


/* =========================================================
   FORM LABELS
   ========================================================= */

[data-testid="stWidgetLabel"] {
    font-weight: 600 !important;
}


/* =========================================================
   INPUT PLACEHOLDER
   ========================================================= */

input::placeholder {
    opacity: 0.75 !important;
}


/* =========================================================
   CARDS
   ========================================================= */

.card {
    padding: 18px;

    border-radius: 15px;

    border: 1px solid #e2e8f0;

    margin-bottom: 12px;
}


/* =========================================================
   MOBILE RESPONSIVE
   ========================================================= */

@media (max-width: 768px) {

    .hero {
        padding: 25px 15px;
    }

    .hero h1 {
        font-size: 32px !important;
    }

    .hero p {
        font-size: 15px !important;
    }

    .hero p strong,
    .hero p b {
        font-size: 17px !important;
    }
}

</style>


<!-- ======================================================
     EDUPATH HERO
     ====================================================== -->

<div class="hero">

    <h1>
        🎓 EduPath Pakistan
    </h1>

    <p>
        <strong>
            AI-Powered Education & Career Guidance
        </strong>
    </p>

    <p>
        Didn't get university admission?
        Your educational journey doesn't have to stop.
    </p>

</div>

""", unsafe_allow_html=True)
