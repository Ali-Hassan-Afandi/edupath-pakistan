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

st.markdown("""
<div class="hero">
<h1>🎓 EduPath Pakistan</h1>
<p><b>AI-Powered Education & Career Guidance</b></p>
<p>Didn't get university admission? Your educational journey doesn't have to stop.</p>
</div>
""", unsafe_allow_html=True)

if "profile" not in st.session_state: st.session_state.profile = {}
if "report" not in st.session_state: st.session_state.report = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []

st.subheader("👤 Student Profile")
with st.form("profile_form"):
    c1,c2 = st.columns(2)
    with c1:
        name = st.text_input("Full Name", placeholder="e.g. Ali Khan")
        education = st.selectbox("Education Level", ["Intermediate","Matric","FSc Pre-Medical","FSc Pre-Engineering","ICS","FA","ICom","A-Level","DAE","Bachelor's","Other"])
        marks = st.text_input("Marks / Percentage", placeholder="e.g. 68%")
        subjects = st.text_input("Major Subjects", placeholder="e.g. Mathematics, Physics, Chemistry")
    with c2:
        city = st.text_input("City", placeholder="e.g. Multan")
        career_goal = st.text_input("Desired Career / Field", placeholder="e.g. Computer Science")
        budget = st.selectbox("Education Budget", ["Very limited","Limited","Moderate","Flexible","Not sure"])
        gap_year = st.radio("Considering a Gap Year?", ["Yes","No","Not sure"], horizontal=True)
    save = st.form_submit_button("💾 Save Student Profile", use_container_width=True)

if save:
    st.session_state.profile = dict(name=name, education=education, marks=marks,
        subjects=subjects, city=city, career_goal=career_goal, budget=budget, gap_year=gap_year)
    st.success("Student profile saved successfully.")

st.divider()
st.subheader("📊 Generate Your Education Report")
st.write("Get a personalized assessment, pathway recommendation, career direction and 90-day action plan.")

if st.button("🚀 Generate My Education Report", type="primary", use_container_width=True):
    if not st.session_state.profile:
        st.warning("Please save your student profile first.")
    else:
        with st.spinner("EduPath is preparing your personalized report..."):
            try:
                st.session_state.report = generate_report(st.session_state.profile)
                st.success("Your report is ready.")
            except Exception as e:
                st.error(f"Could not generate the report: {e}")

if st.session_state.report:
    st.divider()
    st.subheader("📄 Your Personalized Report")
    st.markdown(st.session_state.report)
    pdf = markdown_to_pdf(st.session_state.report)
    txt = st.session_state.report.encode("utf-8")
    d1,d2 = st.columns(2)
    with d1:
        st.download_button("⬇️ Download Report as PDF", pdf,
            "EduPath_Pakistan_Education_Report.pdf", "application/pdf",
            use_container_width=True)
    with d2:
        st.download_button("⬇️ Download Report as TXT", txt,
            "EduPath_Pakistan_Education_Report.txt", "text/plain",
            use_container_width=True)

st.divider()
st.subheader("💬 AI Education Counselor")
st.write("Ask questions about education, careers, university strategy, skills or gap years.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_message = st.chat_input("Ask your education counselor...")
if user_message:
    if not st.session_state.profile:
        st.warning("Please save your student profile before starting the chat.")
    else:
        st.session_state.chat_history.append({"role":"user","content":user_message})
        with st.chat_message("user"): st.markdown(user_message)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = counselor_reply(st.session_state.profile,
                                             st.session_state.chat_history[:-1],
                                             user_message)
                    st.markdown(answer)
                    st.session_state.chat_history.append({"role":"assistant","content":answer})
                except Exception as e:
                    st.error(f"Could not contact the AI counselor: {e}")

st.divider()
st.subheader("🗺️ EduPath 90-Day Framework")
c1,c2,c3 = st.columns(3)
with c1: st.markdown("### 📅 Days 1–30\n**UNDERSTAND**\n\n- Assess options\n- Identify suitable fields\n- Research programs\n- Identify skill gaps")
with c2: st.markdown("### 📅 Days 31–60\n**PREPARE**\n\n- Build relevant skills\n- Prepare applications\n- Improve profile\n- Explore financial options")
with c3: st.markdown("### 📅 Days 61–90\n**ACT**\n\n- Apply to opportunities\n- Start projects\n- Contact institutions\n- Review progress")

st.info("⚠️ EduPath provides AI-based informational guidance. Always verify current admission requirements, fees, deadlines, eligibility and scholarship information through official sources.")
st.caption("EduPath Pakistan — Helping students answer: “What should I do next?”")
