# ============================================================
# EDUPATH PAKISTAN
# Complete Streamlit Application
# ============================================================

import os
import re
from io import BytesIO

import streamlit as st
from groq import Groq

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.units import inch


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="EduPath Pakistan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ==========================================================
   GLOBAL
   ========================================================== */

html, body, [class*="css"] {
    font-family: "Inter", "Segoe UI", Arial, sans-serif;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

/* ==========================================================
   HERO
   ========================================================== */

.edupath-hero {
    background: linear-gradient(
        135deg,
        #eef4ff 0%,
        #f8fbff 55%,
        #e6efff 100%
    );

    border: 1px solid #d8e5ff;
    border-radius: 24px;

    padding: 44px 30px;
    margin-bottom: 28px;

    text-align: center;

    box-shadow:
        0 10px 35px rgba(15, 23, 42, 0.08);
}

.edupath-title {
    color: #1e40af !important;

    font-size: 46px;
    line-height: 1.15;

    font-weight: 800;

    margin: 0 0 12px 0;
}

.edupath-subtitle {
    color: #0f172a !important;

    font-size: 21px;

    font-weight: 700;

    margin-bottom: 10px;
}

.edupath-description {
    color: #475569 !important;

    font-size: 16px;

    font-weight: 500;
}


/* ==========================================================
   INFO CARDS
   ========================================================== */

.feature-card {
    background: rgba(255, 255, 255, 0.95);

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 22px;

    min-height: 145px;

    box-shadow:
        0 5px 18px rgba(15, 23, 42, 0.06);

    margin-bottom: 8px;
}

.feature-card h3 {
    color: #0f172a !important;

    margin-top: 0;

    margin-bottom: 10px;

    font-size: 18px;
}

.feature-card p {
    color: #475569 !important;

    font-size: 14px;

    line-height: 1.6;
}


/* ==========================================================
   STATUS CARD
   ========================================================== */

.profile-status {
    background: #eff6ff;

    border-left: 5px solid #2563eb;

    border-radius: 12px;

    padding: 14px 16px;

    color: #1e3a8a !important;

    margin-bottom: 15px;
}


/* ==========================================================
   SECTION HEADINGS
   ========================================================== */

.section-title {
    font-size: 27px;

    font-weight: 800;

    margin-top: 4px;

    margin-bottom: 5px;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton > button {
    border-radius: 12px;

    min-height: 46px;

    font-weight: 700;

    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
}


/* ==========================================================
   DOWNLOAD BUTTONS
   ========================================================== */

.stDownloadButton > button {
    border-radius: 12px;

    min-height: 44px;

    font-weight: 700;
}


/* ==========================================================
   FORM
   ========================================================== */

[data-testid="stForm"] {
    border: 1px solid rgba(148, 163, 184, 0.25);

    border-radius: 16px;

    padding: 18px;
}


/* ==========================================================
   INPUT LABELS
   ========================================================== */

[data-testid="stWidgetLabel"] p {
    font-weight: 650;
}


/* ==========================================================
   REPORT CONTAINER
   ========================================================== */

.report-header {
    background: linear-gradient(
        135deg,
        #1d4ed8,
        #2563eb
    );

    border-radius: 16px;

    padding: 20px 22px;

    color: white !important;

    margin-top: 12px;

    margin-bottom: 18px;
}

.report-header h3 {
    color: white !important;

    margin: 0 0 5px 0;
}

.report-header p {
    color: #dbeafe !important;

    margin: 0;
}


/* ==========================================================
   CHAT
   ========================================================== */

[data-testid="stChatMessage"] {
    border-radius: 14px;

    padding: 6px;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {
    border-right: 1px solid rgba(148, 163, 184, 0.18);
}

.sidebar-title {
    font-size: 24px;

    font-weight: 800;

    margin-bottom: 3px;
}

.sidebar-subtitle {
    font-size: 13px;

    opacity: 0.72;

    margin-bottom: 20px;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.edupath-footer {
    text-align: center;

    opacity: 0.70;

    font-size: 13px;

    padding: 25px 5px 10px 5px;
}


/* ==========================================================
   MOBILE RESPONSIVENESS
   ========================================================== */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .edupath-hero {
        padding: 30px 18px;
    }

    .edupath-title {
        font-size: 33px;
    }

    .edupath-subtitle {
        font-size: 17px;
    }

    .edupath-description {
        font-size: 14px;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are EduPath Pakistan, an AI-powered education and career
counselor designed for students in Pakistan.

Your job is to help students make realistic decisions about
education, careers, skills and alternative pathways.

You may communicate in:
- English
- Urdu
- Roman Urdu

IMPORTANT RULES:

1. Never guarantee university admission.

2. Never guarantee employment.

3. Never invent:
   - university admission requirements
   - merit percentages
   - fees
   - admission deadlines
   - scholarship amounts
   - current eligibility criteria

4. If current institutional information is needed, clearly tell
the student to verify it from the official university,
government, scholarship or institution website.

5. University is not the only valid pathway.

Consider:
- Public universities
- Private universities
- Technical education
- Vocational education
- DAE
- Professional certifications
- Online learning
- Skills training
- Internships
- Freelancing
- Entrepreneurship
- Structured gap years

6. Never discourage students only because of low marks.

7. Recommendations should consider:
   - academic level
   - marks
   - subjects
   - city
   - career goal
   - budget
   - gap-year preference

8. Give realistic priorities instead of a random list.

9. When useful, provide:
   - Primary pathway
   - Alternative pathways
   - Advantages
   - Limitations
   - Skills
   - Immediate actions
   - 90-day roadmap

10. Use simple, supportive and practical language.

The central question you must answer is:

"What should this student do next?"
"""


# ============================================================
# SESSION STATE
# ============================================================

if "profile" not in st.session_state:
    st.session_state.profile = {}

if "report" not in st.session_state:
    st.session_state.report = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# GROQ CLIENT
# ============================================================

@st.cache_resource
def get_groq_client():

    try:
        api_key = st.secrets.get(
            "GROQ_API_KEY",
            os.environ.get("GROQ_API_KEY"),
        )
    except Exception:
        api_key = os.environ.get("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# ============================================================
# MODEL SELECTION
# ============================================================

@st.cache_data(ttl=3600)
def get_model_name():

    try:
        configured_model = st.secrets.get(
            "GROQ_MODEL",
            "",
        )
    except Exception:
        configured_model = ""

    if configured_model:
        return configured_model

    return "openai/gpt-oss-120b"


# ============================================================
# BUILD PROFILE
# ============================================================

def build_profile(profile):

    return f"""
STUDENT PROFILE

Name:
{profile.get("name") or "Not provided"}

Education:
{profile.get("education") or "Not provided"}

Marks / Percentage:
{profile.get("marks") or "Not provided"}

Major Subjects:
{profile.get("subjects") or "Not provided"}

City:
{profile.get("city") or "Not provided"}

Desired Career / Field:
{profile.get("career_goal") or "Not provided"}

Education Budget:
{profile.get("budget") or "Not provided"}

Considering Gap Year:
{profile.get("gap_year") or "Not provided"}
"""


# ============================================================
# CALL GROQ
# ============================================================

def call_groq(
    messages,
    max_tokens=2000,
    temperature=0.4,
):

    client = get_groq_client()

    if client is None:
        raise RuntimeError(
            "Groq API key is missing. "
            "Add GROQ_API_KEY in Streamlit App Secrets."
        )

    model = get_model_name()

    try:

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        return response.choices[0].message.content

    except Exception as error:

        raise RuntimeError(
            f"Groq API error using model '{model}': {error}"
        )


# ============================================================
# REPORT GENERATION
# ============================================================

def generate_report(profile):

    prompt = f"""
Create a detailed personalized education and career guidance
report for this Pakistani student.

{build_profile(profile)}

Use the following exact structure:


# EduPath Pakistan - Personalized Education Report


## 1. Student Profile

Briefly summarize the student's current background.


## 2. Current Situation Analysis

Explain the student's current position and the main decision
they need to make.


## 3. Recommended Primary Pathway

Give ONE main recommendation.

Explain:

- Why it fits
- What the student should focus on
- Main benefits
- Main limitations


## 4. Alternative Pathways

Provide 2 to 4 realistic alternatives.

For each include:

- Pathway
- Why it may fit
- Advantage
- Limitation


## 5. Career Direction

Explain suitable career directions based on:

- Academic background
- Interests
- Desired career
- Financial situation


## 6. Skills to Develop

Separate into:

### Short-Term Skills

### Medium-Term Skills


## 7. University Strategy

Explain how the student should approach university education
if it is appropriate.

Do not invent specific current requirements, merit, fees,
deadlines or scholarships.

Tell the student to verify current information from official
sources.


## 8. Financial Strategy

Consider the student's budget.

Discuss appropriate possibilities including:

- Public universities
- Lower-cost options
- Financial aid
- Scholarships
- Skills pathways
- Certifications


## 9. 90-Day Action Plan

### Days 1-30: Understand

Give concrete actions.

### Days 31-60: Prepare

Give concrete actions.

### Days 61-90: Act

Give concrete actions.


## 10. Risks and Things to Verify

Clearly identify information that needs official verification.


## 11. Five Immediate Next Steps

Give exactly five prioritized actions.


## 12. Final Guidance

End with a short realistic and motivating conclusion.


IMPORTANT:

Do not fabricate facts.

Do not guarantee admission.

Do not guarantee employment.

Prioritize practical action.

Use simple language.
"""

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    return call_groq(
        messages=messages,
        max_tokens=4000,
        temperature=0.3,
    )


# ============================================================
# COUNSELOR
# ============================================================

def counselor_reply(
    profile,
    chat_history,
    message,
):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "system",
            "content": build_profile(profile),
        },
    ]

    # Keep recent conversation
    for item in chat_history[-12:]:

        if item.get("role") in [
            "user",
            "assistant",
        ]:

            messages.append(
                {
                    "role": item["role"],
                    "content": item["content"],
                }
            )

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    return call_groq(
        messages=messages,
        max_tokens=1800,
        temperature=0.4,
    )


# ============================================================
# PDF HELPERS
# ============================================================

def clean_pdf_text(text):

    # Remove emoji and other unsupported symbols for
    # ReportLab's standard fonts.

    return re.sub(
        r"[^\x00-\x7F]+",
        " ",
        text,
    )


def markdown_to_pdf(text):

    text = clean_pdf_text(text)

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title="EduPath Pakistan Education Report",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "EduPathTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=18,
        leading=23,
        spaceAfter=18,
        textColor="#1d4ed8",
    )

    h2_style = ParagraphStyle(
        "EduPathH2",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        spaceBefore=12,
        spaceAfter=7,
        textColor="#0f172a",
    )

    h3_style = ParagraphStyle(
        "EduPathH3",
        parent=styles["Heading3"],
        fontSize=11,
        leading=15,
        spaceBefore=8,
        spaceAfter=5,
    )

    body_style = ParagraphStyle(
        "EduPathBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=14,
        spaceAfter=6,
    )

    story = []

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:

            story.append(
                Spacer(
                    1,
                    5,
                )
            )

            continue

        safe = (
            line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        if line.startswith("# "):

            story.append(
                Paragraph(
                    safe[2:],
                    title_style,
                )
            )

        elif line.startswith("## "):

            story.append(
                Paragraph(
                    safe[3:],
                    h2_style,
                )
            )

        elif line.startswith("### "):

            story.append(
                Paragraph(
                    safe[4:],
                    h3_style,
                )
            )

        elif line.startswith("- "):

            story.append(
                Paragraph(
                    "• " + safe[2:],
                    body_style,
                )
            )

        else:

            story.append(
                Paragraph(
                    safe,
                    body_style,
                )
            )

    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# SIDEBAR PROFILE
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🎓 EduPath</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Build your student profile before generating guidance.'
        '</div>',
        unsafe_allow_html=True,
    )

    with st.form(
        "student_profile_form",
        clear_on_submit=False,
    ):

        name = st.text_input(
            "Full Name",
            value=st.session_state.profile.get(
                "name",
                "",
            ),
            placeholder="e.g. Ali Khan",
        )

        education_options = [
            "Intermediate",
            "Matric",
            "FSc Pre-Medical",
            "FSc Pre-Engineering",
            "ICS",
            "FA",
            "ICom",
            "A-Level",
            "DAE",
            "Bachelor's",
            "Other",
        ]

        current_education = (
            st.session_state.profile.get(
                "education",
                "Intermediate",
            )
        )

        try:
            education_index = education_options.index(
                current_education
            )
        except ValueError:
            education_index = 0

        education = st.selectbox(
            "Education Level",
            education_options,
            index=education_index,
        )

        marks = st.text_input(
            "Marks / Percentage",
            value=st.session_state.profile.get(
                "marks",
                "",
            ),
            placeholder="e.g. 68%",
        )

        subjects = st.text_input(
            "Major Subjects",
            value=st.session_state.profile.get(
                "subjects",
                "",
            ),
            placeholder="Mathematics, Physics...",
        )

        city = st.text_input(
            "City",
            value=st.session_state.profile.get(
                "city",
                "",
            ),
            placeholder="e.g. Multan",
        )

        career_goal = st.text_input(
            "Desired Career / Field",
            value=st.session_state.profile.get(
                "career_goal",
                "",
            ),
            placeholder="e.g. Computer Science",
        )

        budget_options = [
            "Very limited",
            "Limited",
            "Moderate",
            "Flexible",
            "Not sure",
        ]

        current_budget = (
            st.session_state.profile.get(
                "budget",
                "Limited",
            )
        )

        try:
            budget_index = budget_options.index(
                current_budget
            )
        except ValueError:
            budget_index = 1

        budget = st.selectbox(
            "Education Budget",
            budget_options,
            index=budget_index,
        )

        gap_options = [
            "Yes",
            "No",
            "Not sure",
        ]

        current_gap = (
            st.session_state.profile.get(
                "gap_year",
                "Not sure",
            )
        )

        try:
            gap_index = gap_options.index(
                current_gap
            )
        except ValueError:
            gap_index = 2

        gap_year = st.radio(
            "Considering Gap Year?",
            gap_options,
            index=gap_index,
        )

        save_profile = st.form_submit_button(
            "💾 Save Student Profile",
            use_container_width=True,
            type="primary",
        )

    if save_profile:

        st.session_state.profile = {
            "name": name.strip(),
            "education": education,
            "marks": marks.strip(),
            "subjects": subjects.strip(),
            "city": city.strip(),
            "career_goal": career_goal.strip(),
            "budget": budget,
            "gap_year": gap_year,
        }

        st.success(
            "Profile saved successfully."
        )

    st.divider()

    if st.session_state.profile:

        st.markdown("### Current Profile")

        st.caption(
            f"🎓 {st.session_state.profile.get('education', '')}"
        )

        if st.session_state.profile.get("career_goal"):

            st.caption(
                "🎯 "
                + st.session_state.profile["career_goal"]
            )

        if st.session_state.profile.get("city"):

            st.caption(
                "📍 "
                + st.session_state.profile["city"]
            )


# ============================================================
# HERO
# IMPORTANT: HTML starts at column 1 to avoid Markdown
# interpreting it as a code block.
# ============================================================

hero_html = """<div class="edupath-hero">
<div class="edupath-title">🎓 EduPath Pakistan</div>
<div class="edupath-subtitle">AI-Powered Education &amp; Career Guidance</div>
<div class="edupath-description">Didn't get university admission? Your educational journey doesn't have to stop.</div>
</div>"""

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# ============================================================
# FEATURE CARDS
# ============================================================

feature1, feature2, feature3 = st.columns(3)

with feature1:

    st.markdown(
        """
<div class="feature-card">
<h3>🎓 Education Pathways</h3>
<p>
Explore realistic university, technical,
vocational and alternative education routes.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

with feature2:

    st.markdown(
        """
<div class="feature-card">
<h3>💼 Career Direction</h3>
<p>
Understand career options based on your
education, interests, budget and goals.
</p>
</div>
""",
        unsafe_allow_html=True,
    )

with feature3:

    st.markdown(
        """
<div class="feature-card">
<h3>🗺️ Personal Roadmap</h3>
<p>
Generate a personalized 30, 60 and 90-day
plan with practical next actions.
</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# MAIN TABS
# ============================================================

report_tab, counselor_tab, roadmap_tab = st.tabs(
    [
        "📊 Personalized Report",
        "💬 AI Counselor",
        "🗺️ 90-Day Framework",
    ]
)


# ============================================================
# REPORT TAB
# ============================================================

with report_tab:

    st.markdown(
        '<div class="section-title">'
        '📊 Personalized Education Report'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Generate an AI-powered analysis based on "
        "the student profile saved in the sidebar."
    )

    if not st.session_state.profile:

        st.info(
            "👈 Complete and save your student profile "
            "from the sidebar first."
        )

    else:

        profile = st.session_state.profile

        summary1, summary2, summary3, summary4 = (
            st.columns(4)
        )

        summary1.metric(
            "Education",
            profile.get(
                "education",
                "Not provided",
            ),
        )

        summary2.metric(
            "Marks",
            profile.get(
                "marks",
                "Not provided",
            ) or "Not provided",
        )

        summary3.metric(
            "Career Goal",
            profile.get(
                "career_goal",
                "Not provided",
            ) or "Not provided",
        )

        summary4.metric(
            "Budget",
            profile.get(
                "budget",
                "Not provided",
            ),
        )

        st.write("")

        generate_report_button = st.button(
            "🚀 Generate My Education Report",
            type="primary",
            use_container_width=True,
        )

        if generate_report_button:

            with st.spinner(
                "Analyzing your profile and building "
                "your personalized roadmap..."
            ):

                try:

                    st.session_state.report = (
                        generate_report(
                            st.session_state.profile
                        )
                    )

                    st.success(
                        "Your personalized report is ready."
                    )

                except Exception as error:

                    st.error(
                        str(error)
                    )

        if st.session_state.report:

            st.markdown(
                """<div class="report-header">
<h3>📄 Your Personalized Guidance Report</h3>
<p>Generated from your saved EduPath student profile.</p>
</div>""",
                unsafe_allow_html=True,
            )

            st.markdown(
                st.session_state.report
            )

            st.divider()

            try:

                pdf_data = markdown_to_pdf(
                    st.session_state.report
                )

            except Exception as pdf_error:

                pdf_data = None

                st.warning(
                    "The report was generated successfully, "
                    f"but PDF creation failed: {pdf_error}"
                )

            text_data = (
                st.session_state.report
                .encode("utf-8")
            )

            download1, download2 = st.columns(2)

            with download1:

                if pdf_data:

                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_data,
                        file_name=(
                            "EduPath_Pakistan_"
                            "Education_Report.pdf"
                        ),
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                    )

            with download2:

                st.download_button(
                    label="📝 Download TXT Report",
                    data=text_data,
                    file_name=(
                        "EduPath_Pakistan_"
                        "Education_Report.txt"
                    ),
                    mime="text/plain",
                    use_container_width=True,
                )


# ============================================================
# COUNSELOR TAB
# ============================================================

with counselor_tab:

    st.markdown(
        '<div class="section-title">'
        '💬 AI Education Counselor'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Ask follow-up questions based on your "
        "saved academic profile."
    )

    if not st.session_state.profile:

        st.info(
            "👈 Save your student profile in the "
            "sidebar before starting the counselor."
        )

    else:

        starter1, starter2, starter3 = (
            st.columns(3)
        )

        if starter1.button(
            "I didn't get admission",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "I didn't get university admission. "
                "What should I do next?"
            )

        if starter2.button(
            "Should I take a gap year?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "Should I take a gap year? "
                "Please analyze it using my profile."
            )

        if starter3.button(
            "What skills should I learn?",
            use_container_width=True,
        ):

            st.session_state.pending_question = (
                "Which skills should I start learning "
                "based on my career goal?"
            )

        st.divider()

        for message in st.session_state.chat_history:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        typed_message = st.chat_input(
            "Ask EduPath about education, careers, skills..."
        )

        pending_message = st.session_state.pop(
            "pending_question",
            None,
        )

        user_message = (
            typed_message
            if typed_message
            else pending_message
        )

        if user_message:

            st.session_state.chat_history.append(
                {
                    "role": "user",
                    "content": user_message,
                }
            )

            with st.chat_message("user"):

                st.markdown(
                    user_message
                )

            with st.chat_message("assistant"):

                with st.spinner(
                    "EduPath is analyzing your question..."
                ):

                    try:

                        answer = counselor_reply(
                            st.session_state.profile,
                            st.session_state.chat_history[:-1],
                            user_message,
                        )

                        st.markdown(
                            answer
                        )

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": answer,
                            }
                        )

                    except Exception as error:

                        st.error(
                            str(error)
                        )

        if st.session_state.chat_history:

            if st.button(
                "🗑️ Clear Conversation",
            ):

                st.session_state.chat_history = []

                st.rerun()


# ============================================================
# ROADMAP TAB
# ============================================================

with roadmap_tab:

    st.markdown(
        '<div class="section-title">'
        '🗺️ EduPath 90-Day Framework'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "A simple framework students can use while "
        "planning their next education or career step."
    )

    phase1, phase2, phase3 = st.columns(3)

    with phase1:

        st.markdown(
            """
### 📘 Days 1–30

#### UNDERSTAND

- Assess your current position
- Identify suitable fields
- Research education pathways
- Compare realistic alternatives
- Identify major skill gaps
- Define your main goal
"""
        )

    with phase2:

        st.markdown(
            """
### 🛠️ Days 31–60

#### PREPARE

- Build relevant skills
- Prepare applications
- Improve your academic profile
- Research financial options
- Start a practical project
- Organize required documents
"""
        )

    with phase3:

        st.markdown(
            """
### 🚀 Days 61–90

#### ACT

- Apply to suitable opportunities
- Contact institutions
- Complete relevant projects
- Review your progress
- Update your strategy
- Prepare the next 90-day cycle
"""
        )

    st.divider()

    st.info(
        """
**Important:** Your AI-generated personalized report
should take priority over this general framework because
it uses your actual academic profile.
"""
    )


# ============================================================
# DISCLAIMER
# ============================================================

st.divider()

st.warning(
    """
⚠️ **Important:** EduPath provides AI-generated informational
guidance. Admission requirements, merit criteria, fees,
deadlines, scholarships and eligibility rules can change.

Always verify current information through official university,
institution or government sources before making a final decision.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """<div class="edupath-footer">
<strong>🎓 EduPath Pakistan</strong><br>
AI-Powered Education &amp; Career Guidance<br><br>
Helping students answer:
<strong>"What should I do next?"</strong>
</div>""",
    unsafe_allow_html=True,
)
