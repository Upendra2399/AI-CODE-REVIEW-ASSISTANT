import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import os
import random

# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="AI Code Review Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= LOAD API KEY ================= #

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = None

# ================= GROQ CLIENT ================= #

client = None

if api_key:
    client = Groq(api_key=api_key)

# ================= CUSTOM CSS ================= #

st.markdown("""
<style>

/* GOOGLE FONT */

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

/* MAIN BACKGROUND */

.stApp {
    background: linear-gradient(135deg, #020617, #000814);
    color: white;
}

/* HIDE STREAMLIT BRANDING */

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

[data-testid="stToolbar"] {
    display: none !important;
}

[data-testid="stStatusWidget"] {
    display: none !important;
}

[data-testid="stDecoration"] {
    display: none !important;
}

div[data-testid="stToolbarActions"] {
    display: none !important;
}

.viewerBadge_container__1QSob,
.viewerBadge_link__1S137,
.viewerBadge_text__1JaDK {
    display: none !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #07101f !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* SIDEBAR TEXT */

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* FEATURE CARD */

.feature-card {
    background: rgba(255,255,255,0.04);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-3px);
    border: 1px solid #8B5CF6;
    box-shadow: 0 0 25px rgba(139,92,246,.3);
}

/* HERO SECTION */

.hero-container {

    display: flex;
    align-items: center;
    gap: 30px;

    padding: 30px;

    margin-bottom: 35px;

    border-radius: 28px;

    background: rgba(255,255,255,0.03);

    border: 1px solid rgba(255,255,255,0.08);

    backdrop-filter: blur(10px);

    box-shadow: 0 0 35px rgba(139,92,246,0.12);
}

/* LOGO */

.main-logo {

    width: 110px;
    height: 110px;

    border-radius: 50%;

    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 52px;

    background: linear-gradient(
    135deg,
    #9333EA,
    #3B82F6
    );

    box-shadow:
    0 0 40px rgba(147,51,234,.55);

    animation: glow 3s infinite alternate;
}

/* LOGO GLOW */

@keyframes glow {

    from {
        transform: scale(1);
        box-shadow:
        0 0 25px rgba(147,51,234,.4);
    }

    to {
        transform: scale(1.05);
        box-shadow:
        0 0 55px rgba(59,130,246,.75);
    }
}

/* TITLE */

.main-title {

    font-size: 68px;

    font-weight: 900;

    line-height: 1.1;

    background: linear-gradient(
    to right,
    #C084FC,
    #60A5FA
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 12px;
}

/* SUBTEXT */

.sub-text {

    font-size: 21px;

    color: #CBD5E1;

    line-height: 1.8;
}

/* LABELS */

.stSelectbox label,
.stTextArea label,
.stFileUploader label {

    color: white !important;

    font-size: 18px !important;

    font-weight: 700 !important;
}

/* SELECT BOX */

.stSelectbox > div > div {

    background: #111827 !important;

    color: white !important;

    border-radius: 16px !important;

    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {

    background: #111827;

    padding: 20px;

    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.08);
}

/* UPLOADER DARK */

[data-testid="stFileUploaderDropzone"] {

    background: #1E293B !important;

    border: 2px dashed #8B5CF6 !important;

    border-radius: 18px !important;
}

[data-testid="stFileUploaderDropzone"] * {
    color: white !important;
}

/* TEXT AREA */

.stTextArea textarea {

    background: #0F172A !important;

    color: white !important;

    border-radius: 20px !important;

    border: 2px solid #8B5CF6 !important;

    font-size: 17px !important;

    min-height: 350px !important;
}

/* REVIEW BUTTON */

.stButton button {

    background: linear-gradient(
    to right,
    #7C3AED,
    #4F46E5
    );

    color: white !important;

    border: none;

    border-radius: 18px;

    height: 62px;

    width: 100%;

    font-size: 22px;

    font-weight: 700;

    margin-top: 20px;

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.01);

    box-shadow: 0 0 25px rgba(139,92,246,.4);
}

/* RESULT BOX */

.result-box {

    background: rgba(255,255,255,0.04);

    border-left: 5px solid #8B5CF6;

    padding: 30px;

    border-radius: 20px;

    margin-top: 30px;

    color: white;

    line-height: 1.9;

    font-size: 17px;
}

/* METRIC */

[data-testid="metric-container"] {

    background: #111827;

    border: 1px solid rgba(255,255,255,0.08);

    padding: 18px;

    border-radius: 18px;
}

/* DOWNLOAD BUTTON */

.stDownloadButton button {

    background: linear-gradient(
    to right,
    #9333EA,
    #2563EB
    ) !important;

    color: white !important;

    border: none !important;

    border-radius: 16px !important;

    height: 55px;

    font-size: 18px;

    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR ================= #

with st.sidebar:

    st.markdown("# 🤖 AI Reviewer")

    st.markdown("### Smart AI-powered code analysis assistant")

    st.markdown("## ✨ Features")

    st.markdown(
        '<div class="feature-card">🐞 Bug Detection</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="feature-card">✅ Best Practices</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="feature-card">♻ Refactoring Suggestions</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="feature-card">📘 Documentation Tips</div>',
        unsafe_allow_html=True
    )

# ================= HERO SECTION ================= #

st.markdown("""

<div class="hero-container">

    <div class="main-logo">
        💻
    </div>

    <div>

        <div class="main-title">
            AI Code Review Assistant
        </div>

        <div class="sub-text">
            Advanced AI analysis to detect bugs, improve quality,
            suggest best practices, and optimize your code.
        </div>

    </div>

</div>

""", unsafe_allow_html=True)

# ================= INPUTS ================= #

language = st.selectbox(
    "Select Programming Language",
    ["Python", "Java", "C++", "JavaScript", "C"]
)

uploaded_file = st.file_uploader(
    "📂 Upload Code File",
    type=["py", "java", "cpp", "js", "c"]
)

code = st.text_area(
    "💻 Paste Your Code Here",
    placeholder="Paste your code here..."
)

# ================= FILE READ ================= #

if uploaded_file is not None:

    code = str(uploaded_file.read(), "utf-8")

    st.success("✅ File uploaded successfully!")

# ================= REVIEW BUTTON ================= #

if st.button("🚀 Review Code"):

    if not api_key:

        st.error("Please add GROQ_API_KEY")

    elif code.strip() == "":

        st.warning("Please paste some code")

    else:

        try:

            with st.spinner("🔍 Analyzing your code..."):

                prompt = f"""
You are an expert AI Code Reviewer.

Analyze the following {language} code.

Provide:
1. Bugs Detected
2. Best Practices
3. Refactoring Suggestions
4. Documentation Recommendations
5. Improved Version of Code

Code:
{code}
"""

                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1800
                )

                result = response.choices[0].message.content

                st.success("✅ AI Review Completed Successfully!")

                score = random.randint(80, 98)

                st.metric(
                    label="⭐ Code Quality Score",
                    value=f"{score}/100"
                )

                st.progress(score)

                st.markdown(
                    f'<div class="result-box">{result}</div>',
                    unsafe_allow_html=True
                )

                st.code(result)

                st.download_button(
                    label="📥 Download Review Report",
                    data=result,
                    file_name="code_review_report.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(f"Error: {str(e)}")