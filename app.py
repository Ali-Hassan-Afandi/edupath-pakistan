# ============================================================
# EDUPATH PAKISTAN
# COMPLETE STREAMLIT APPLICATION
# ============================================================

import os
from io import BytesIO

import streamlit as st
from groq import Groq

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.units import inch


# ============================================================
# STREAMLIT PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EduPath Pakistan",
    page_icon="🎓",
    layout="wide"
)


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are EduPath Pakistan, an AI-powered education and career
counselor designed specifically for students in Pakistan.

Your mission is to help students understand realistic
education, career and skills pathways.

You may communicate in:
- English
- Urdu
- Roman Urdu

IMPORTANT PRINCIPLES:

1. Never guarantee university admission.

2. Never invent:
   - university admission requirements
   - fees
   - deadlines
   - scholarships
   - eligibility criteria

3. If current university information is required,
tell the student to verify it through the institution's
official source.

4. University is not the only possible pathway.

Consider:
- Public universities
- Private universities
- Technical education
- Vocational education
- DAE
- Professional certifications
- Online learning
- Skills development
- Internships
- Freelancing
- Entrepreneurship
- Gap-year preparation

5. Do not discourage students because of low marks.

6. Explain realistic options clearly.

7. Focus on:

"WHAT SHOULD THIS STUDENT DO NEXT?"

8. Recommendations should consider:
- Education
- Marks
- Subjects
- City
- Career goal
- Budget
- Gap year preference

9. When appropriate provide:
- Primary recommendation
- Alternative options
- Advantages
- Disadvantages
- Skills
- Action plan

10. Keep language simple and practical.

11. Never fabricate facts.

12. When information is uncertain, explicitly say that
it needs to be verified.
"""


# ============================================================
# GET GROQ CLIENT
# ============================================================

def get_client():

    try:

        api_key = st.secrets.get(
            "GROQ_API_KEY",
            os.environ.get("GROQ_API_KEY")
        )

    except Exception:

        api_key = os.environ.get("GROQ_API_KEY")


    if not api_key:

        return None


    return Groq(
        api_key=api_key
    )


# ============================================================
# BUILD STUDENT PROFILE
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
# GROQ CALL
# ============================================================

def call_groq(
    messages,
    max_tokens=2000,
    temperature=0.4
):

    client = get_client()


    if client is None:

        raise RuntimeError(
            "GROQ_API_KEY is not configured. "
            "Please add it in Streamlit Secrets."
        )


    try:

        model = st.secrets.get(
            "GROQ_MODEL",
            "openai/gpt-oss-120b"
        )

    except Exception:

        model = "openai/gpt-oss-120b"


    response = client.chat.completions.create(

        model=model,

        messages=messages,

        temperature=temperature,

        max_tokens=max_tokens
    )


    return response.choices[0].message.content


# ============================================================
# GENERATE REPORT
# ============================================================

def generate_report(profile):

    report_prompt = f"""
Create a personalized education and career guidance report
for the following Pakistani student.

{build_profile(profile)}

Return the report using this structure:

# 🎓 EduPath Pakistan — Personalized Education Report


## 1. Student Profile

Summarize the student's academic background.


## 2. Situation Analysis

Explain the student's current position.


## 3. Recommended Primary Pathway

Explain:

- Why this pathway fits
- What the student should do
- What they should avoid


## 4. Alternative Pathways

Provide 2 to 4 realistic alternatives.

For each alternative include:

- Pathway
- Why it may work
- Main advantage
- Main limitation


## 5. Career Direction

Discuss suitable career and skill directions.


## 6. Skills to Develop

Separate into:

- Short-term skills
- Medium-term skills


## 7. University Strategy

Explain how the student should approach university
applications if appropriate.

Do not invent admission requirements, fees or deadlines.


## 8. Financial Strategy

Consider:

- Public universities
- Scholarships
- Financial aid
- Lower-cost education
- Certifications
- Skills pathways


## 9. 90-Day Action Plan


### Days 1–30 — Understand

Provide specific actions.


### Days 31–60 — Prepare

Provide specific actions.


### Days 61–90 — Act

Provide specific actions.


## 10. Risks & Things to Verify

List information that must be checked independently.


## 11. Immediate Next Steps

Give the student the five most important actions.


## 12. Encouragement

End with a short realistic and constructive message.


IMPORTANT:

- Do not fabricate facts.
- Do not guarantee admission.
- Do not guarantee employment.
- Use simple language.
- Do not assume university is the only option.
- Tell the student to verify current information
  through official sources.
"""


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": report_prompt
        }

    ]


    return call_groq(

        messages=messages,

        max_tokens=4000,

        temperature=0.3
    )


# ============================================================
# AI COUNSELOR
# ============================================================

def counselor_reply(
    profile,
    chat_history,
    message
):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "system",
            "content": build_profile(profile)
        }

    ]


    for item in chat_history:

        if item.get("role") in [
            "user",
            "assistant"
        ]:

            messages.append(item)


    messages.append(

        {
            "role": "user",
            "content": message
        }

    )


    return call_groq(

        messages=messages,

        max_tokens=1800,

        temperature=0.4
    )


# ============================================================
# PDF CREATION
# ============================================================

def markdown_to_pdf(text):

    buffer = BytesIO()


    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=0.65 * inch,

        leftMargin=0.65 * inch,

        topMargin=0.65 * inch,

        bottomMargin=0.65 * inch
    )


    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        alignment=TA_CENTER,

        fontSize=18,

        leading=22,

        spaceAfter=16
    )


    heading_style = ParagraphStyle(

        "ReportHeading",

        parent=styles["Heading2"],

        fontSize=13,

        leading=17,

        spaceBefore=10,

        spaceAfter=6
    )


    body_style = ParagraphStyle(

        "ReportBody",

        parent=styles["BodyText"],

        fontSize=9.5,

        leading=14,

        spaceAfter=6
    )


    story = []


    for raw_line in text.splitlines():

        line = raw_line.strip()


        if not line:

            story.append(
                Spacer(
                    1,
                    5
                )
            )

            continue


        safe_line = (

            line
            .replace(
                "&",
                "&amp;"
            )
            .replace(
                "<",
                "&lt;"
            )
            .replace(
                ">",
                "&gt;"
            )

        )


        if line.startswith("# "):

            story.append(

                Paragraph(
                    safe_line[2:],
                    title_style
                )

            )


        elif line.startswith("## "):

            story.append(

                Paragraph(
                    safe_line[3:],
                    heading_style
                )

            )


        elif line.startswith("### "):

            story.append(

                Paragraph(
                    safe_line[4:],
                    heading_style
                )

            )


        elif line.startswith("- "):

            story.append(

                Paragraph(
                    "• " + safe_line[2:],
                    body_style
                )

            )


        else:

            story.append(

                Paragraph(
                    safe_line,
                    body_style
                )

            )


    document.build(story)


    buffer.seek(0)


    return buffer.getvalue()


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>


/* =========================================================
   HERO
   ========================================================= */

.hero {

    padding: 35px 25px;

    border-radius: 20px;

    text-align: center;

    background: linear-gradient(
        135deg,
        #eff6ff 0%,
        #f8fafc 55%,
        #e0ecff 100%
    );

    border: 1px solid #dbeafe;

    margin-top: 10px;

    margin-bottom: 30px;

    box-shadow:
        0 4px 18px
        rgba(
            0,
            0,
            0,
            0.08
        );
}


/* =========================================================
   HERO TITLE
   ========================================================= */

.hero-title {

    color: #1d4ed8 !important;

    font-size: 42px !important;

    font-weight: 800 !important;

    line-height: 1.2 !important;

    margin: 0 0 14px 0 !important;
}


/* =========================================================
   HERO SUBTITLE
   ========================================================= */

.hero-subtitle {

    color: #0f172a !important;

    font-size: 20px !important;

    font-weight: 700 !important;

    line-height: 1.5 !important;

    margin: 8px 0 !important;
}


/* =========================================================
   HERO DESCRIPTION
   ========================================================= */

.hero-description {

    color: #334155 !important;

    font-size: 17px !important;

    font-weight: 500 !important;

    line-height: 1.6 !important;

    margin: 8px 0 0 0 !important;
}


/* =========================================================
   STREAMLIT HEADINGS
   ========================================================= */

[data-testid="stHeading"] {

    font-weight: 700;
}


/* =========================================================
   INPUT LABELS
   ========================================================= */

[data-testid="stWidgetLabel"] {

    font-weight: 600 !important;
}


/* =========================================================
   FORM BORDER
   ========================================================= */

[data-testid="stForm"] {

    border-radius: 15px !important;

    padding: 20px !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton button {

    border-radius: 10px !important;

    font-weight: 600 !important;
}


/* =========================================================
   DOWNLOAD BUTTONS
   ========================================================= */

.stDownloadButton button {

    border-radius: 10px !important;

    font-weight: 600 !important;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 768px) {

    .hero {

        padding: 25px 15px;

    }


    .hero-title {

        font-size: 31px !important;

    }


    .hero-subtitle {

        font-size: 17px !important;

    }


    .hero-description {

        font-size: 15px !important;

    }

}


</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HERO HTML
# ============================================================

st.markdown(
    """
<div class="hero">

    <div class="hero-title">

        🎓 EduPath Pakistan

    </div>


    <div class="hero-subtitle">

        AI-Powered Education & Career Guidance

    </div>


    <div class="hero-description">

        Didn't get university admission?
        Your educational journey doesn't have to stop.

    </div>

</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE SESSION STATE
# ============================================================

if "profile" not in st.session_state:

    st.session_state.profile = {}


if "report" not in st.session_state:

    st.session_state.report = None


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# ============================================================
# STUDENT PROFILE
# ============================================================

st.subheader(
    "👤 Student Profile"
)


st.write(
    "Enter your information so EduPath can provide "
    "personalized education and career guidance."
)


with st.form(
    "student_profile_form"
):


    column1, column2 = st.columns(2)


    with column1:


        name = st.text_input(

            "Full Name",

            placeholder="e.g. Ali Khan"
        )


        education = st.selectbox(

            "Education Level",

            [

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

                "Other"

            ]
        )


        marks = st.text_input(

            "Marks / Percentage",

            placeholder="e.g. 68%"
        )


        subjects = st.text_input(

            "Major Subjects",

            placeholder=(
                "e.g. Mathematics, "
                "Physics, Chemistry"
            )
        )


    with column2:


        city = st.text_input(

            "City",

            placeholder="e.g. Multan"
        )


        career_goal = st.text_input(

            "Desired Career / Field",

            placeholder="e.g. Computer Science"
        )


        budget = st.selectbox(

            "Education Budget",

            [

                "Very limited",

                "Limited",

                "Moderate",

                "Flexible",

                "Not sure"

            ]
        )


        gap_year = st.radio(

            "Considering a Gap Year?",

            [

                "Yes",

                "No",

                "Not sure"

            ],

            horizontal=True
        )


    save_profile = st.form_submit_button(

        "💾 Save Student Profile",

        use_container_width=True
    )


# ============================================================
# SAVE PROFILE
# ============================================================

if save_profile:


    st.session_state.profile = {

        "name": name,

        "education": education,

        "marks": marks,

        "subjects": subjects,

        "city": city,

        "career_goal": career_goal,

        "budget": budget,

        "gap_year": gap_year

    }


    st.success(
        "Student profile saved successfully."
    )


# ============================================================
# GENERATE REPORT
# ============================================================

st.divider()


st.subheader(
    "📊 Generate Your Education Report"
)


st.write(
    """
Generate a personalized assessment of your education
situation, career direction, alternative pathways and
90-day action plan.
"""
)


generate_button = st.button(

    "🚀 Generate My Education Report",

    type="primary",

    use_container_width=True
)


if generate_button:


    if not st.session_state.profile:


        st.warning(
            "Please save your student profile first."
        )


    else:


        with st.spinner(
            "EduPath is preparing your personalized report..."
        ):


            try:


                report = generate_report(
                    st.session_state.profile
                )


                st.session_state.report = report


                st.success(
                    "Your education report is ready."
                )


            except Exception as error:


                st.error(
                    f"Could not generate report: {error}"
                )


# ============================================================
# DISPLAY REPORT
# ============================================================

if st.session_state.report:


    st.divider()


    st.subheader(
        "📄 Your Personalized Report"
    )


    st.markdown(
        st.session_state.report
    )


    # --------------------------------------------------------
    # CREATE DOWNLOAD FILES
    # --------------------------------------------------------

    try:


        pdf_data = markdown_to_pdf(
            st.session_state.report
        )


    except Exception as pdf_error:


        pdf_data = None


        st.warning(
            f"PDF generation issue: {pdf_error}"
        )


    txt_data = (
        st.session_state.report
        .encode("utf-8")
    )


    download_column1, download_column2 = (
        st.columns(2)
    )


    with download_column1:


        if pdf_data:


            st.download_button(

                label="⬇️ Download Report as PDF",

                data=pdf_data,

                file_name=(
                    "EduPath_Pakistan_"
                    "Education_Report.pdf"
                ),

                mime="application/pdf",

                use_container_width=True
            )


    with download_column2:


        st.download_button(

            label="⬇️ Download Report as TXT",

            data=txt_data,

            file_name=(
                "EduPath_Pakistan_"
                "Education_Report.txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


# ============================================================
# AI COUNSELOR
# ============================================================

st.divider()


st.subheader(
    "💬 AI Education Counselor"
)


st.write(
    """
Ask questions about your education, career,
university strategy, skills, scholarships or gap year.
"""
)


# ============================================================
# DISPLAY PREVIOUS CHAT
# ============================================================

for chat_message in st.session_state.chat_history:


    with st.chat_message(
        chat_message["role"]
    ):


        st.markdown(
            chat_message["content"]
        )


# ============================================================
# CHAT INPUT
# ============================================================

user_message = st.chat_input(
    "Ask your education counselor..."
)


if user_message:


    if not st.session_state.profile:


        st.warning(
            "Please save your student profile "
            "before starting the chat."
        )


    else:


        # ----------------------------------------------------
        # ADD USER MESSAGE
        # ----------------------------------------------------

        st.session_state.chat_history.append(

            {

                "role": "user",

                "content": user_message

            }

        )


        with st.chat_message(
            "user"
        ):


            st.markdown(
                user_message
            )


        # ----------------------------------------------------
        # GET AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):


            with st.spinner(
                "EduPath is thinking..."
            ):


                try:


                    response = counselor_reply(

                        profile=st.session_state.profile,

                        chat_history=(
                            st.session_state.chat_history[:-1]
                        ),

                        message=user_message
                    )


                    st.markdown(
                        response
                    )


                    st.session_state.chat_history.append(

                        {

                            "role": "assistant",

                            "content": response

                        }

                    )


                except Exception as error:


                    st.error(
                        f"AI counselor error: {error}"
                    )


# ============================================================
# 90 DAY FRAMEWORK
# ============================================================

st.divider()


st.subheader(
    "🗺️ EduPath 90-Day Framework"
)


framework1, framework2, framework3 = (
    st.columns(3)
)


with framework1:


    st.markdown(
        """
### 📅 Days 1–30

**UNDERSTAND**

- Assess your options
- Identify suitable fields
- Research programs
- Identify skill gaps
"""
    )


with framework2:


    st.markdown(
        """
### 📅 Days 31–60

**PREPARE**

- Build relevant skills
- Prepare applications
- Improve your academic profile
- Explore financial options
"""
    )


with framework3:


    st.markdown(
        """
### 📅 Days 61–90

**ACT**

- Apply to opportunities
- Start projects
- Contact institutions
- Review your progress
"""
    )


# ============================================================
# IMPORTANT NOTICE
# ============================================================

st.divider()


st.warning(
    """
EduPath provides AI-based informational guidance.

Always verify current:

• Admission requirements  
• Fees  
• Deadlines  
• Eligibility  
• Scholarships  

through official university or institution sources.
"""
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<br>

<div style="
text-align:center;
opacity:0.75;
padding:20px;
">

<b>🎓 EduPath Pakistan</b>

<br>

AI-Powered Education & Career Guidance

<br><br>

Helping students answer:

<b>"What should I do next?"</b>

</div>

""",
    unsafe_allow_html=True
)
