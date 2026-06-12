import streamlit as st
from utils import extractResumeText
from model import analyze_jobs,recommend_resources

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="CareerLens",
    layout="wide"
)

THEME_COLOR = "#3F3DE0"

# ================== STYLES ==================
st.markdown(
    f"""
<link rel="stylesheet"
 href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&display=swap');

body {{
    background-color: #ffffff;
}}

/* ================= HERO ================= */
.hero {{
    position: relative;
    height: 520px;
    font-family: 'Poppins', sans-serif;
}}

.center {{
    position: absolute;
    top: 36%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    animation: fadeUp 1.4s ease-out;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translate(-50%, -60%); }}
    to {{ opacity: 1; transform: translate(-50%, -50%); }}
}}

/* ================= TITLE ================= */
.title {{
    font-size: 62px;
    font-weight: 700;
    color: {THEME_COLOR};
}}

.logo {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}

.logo i {{
    font-size: 40px;
    position: relative;
    top: 2px;
}}

/* ================= DIVIDER ================= */
.divider {{
    width: 110px;
    height: 3px;
    background: linear-gradient(90deg, {THEME_COLOR}, #8B8AF8);
    margin: 18px auto;
    border-radius: 99px;
}}

/* ================= KEYWORDS ================= */
.keywords {{
    display: flex;
    justify-content: center;
    gap: 4px;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
    white-space: nowrap;
    flex-wrap: nowrap;
}}
.keywords {{
    overflow-x: auto;
}}

.keywords span:nth-child(1) {{ color: #16A34A; }}
.keywords span:nth-child(2) {{ color: #F59E0B; }}
.keywords span:nth-child(3) {{ color: #2563EB; }}

.keywords span::after {{
    content: "·";
    margin-left: 16px;
    color: #CBD5E1;
}}

.keywords span:last-child::after {{
    content: "";
}}

/* ================= INFO BOX ================= */
.info-box {{
    margin-top: 16px;
    background: #DAE3EB;
    padding: 18px 26px;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
    font-size: 18px;
    color: #07121E;
    max-width: 620px;
    margin-left: auto;
    margin-right: auto;
}}

/* ================= CTA ================= */
.cta-box {{
    margin: 34px auto 0;
    max-width: 420px;
    padding: 14px 22px;
    border-radius: 14px;
    background: linear-gradient(90deg, #4F46E5, #6366F1);
    box-shadow: 0 18px 40px rgba(79,70,229,0.35);
}}

.cta-box a {{
    color: #ffffff !important;
    font-size: 15px;
    font-weight: 700;
    text-decoration: none !important;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
}}

.cta-box a:visited,
.cta-box a:hover,
.cta-box a:active {{
    color: #ffffff !important;
    text-decoration: none !important;
}}
.cta-box i {{
    animation: bounceDown 1.6s infinite;
}}
@keyframes bounceDown {{
    0%, 100% {{
        transform: translateY(0);
    }}
    50% {{
        transform: translateY(8px);
    }}
}}


/* ================= FLOATING ICONS ================= */
.icon {{
    position: absolute;
    font-size: 34px;
    color: {THEME_COLOR};
    opacity: 0.85;
    animation: float 6s ease-in-out infinite;
}}

@keyframes float {{
    0% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-18px); }}
    100% {{ transform: translateY(0); }}
}}

.l1 {{ top: 40px; left: 90px; }}
.l2 {{ top: 140px; left: 40px; animation-delay: 1s; }}
.l3 {{ top: 260px; left: 95px; animation-delay: 2s; }}
.l4 {{ top: 380px; left: 50px; animation-delay: 3s; }}

.r1 {{ top: 40px; right: 90px; }}
.r2 {{ top: 140px; right: 40px; animation-delay: 1s; }}
.r3 {{ top: 260px; right: 95px; animation-delay: 2s; }}
.r4 {{ top: 380px; right: 50px; animation-delay: 3s; }}

/* ================= FORM SECTION ================= */
.form-section {{
    padding: 50px 0;
    margin-top: 30px;
}}


.stTextInput input {{
    border-radius: 12px !important;
    padding: 12px !important;
    font-size: 17px !important;
}}

.stForm button {{
    font-size: 16px !important;
    font-weight: 600 !important;
    padding: 10px 22px !important;
    border-radius: 10px !important;
    background: linear-gradient(90deg, {THEME_COLOR}, #6366F1) !important;
    color: white !important;
    border: none !important;
}}
/* ================= FOOTER ================= */
.footer {
    text-align: center;
    margin-top: 50px;
    padding: 20px;
    background-color: #ffffff;
    border-top: 1px solid #e5e7eb;
    font-size: 14px;
    color: #6b7280;
    font-family: 'Poppins', sans-serif;
}
</style>
""",
    unsafe_allow_html=True
)

# ================= HERO =================
st.markdown(
    """
<div class="hero">
    <i class="icon l1 fa-solid fa-laptop-code"></i>
    <i class="icon l2 fa-solid fa-database"></i>
    <i class="icon l3 fa-solid fa-chart-line"></i>
    <i class="icon l4 fa-solid fa-code"></i>
    <i class="icon r1 fa-solid fa-briefcase"></i>
    <i class="icon r2 fa-solid fa-user-tie"></i>
    <i class="icon r3 fa-solid fa-house-laptop"></i>
    <i class="icon r4 fa-solid fa-clipboard-list"></i>
    <div class="center">
        <div class="title">
            <span class="logo">
                <i class="fa-solid fa-magnifying-glass"></i>
                CareerLens
            </span>
        </div>
        <div class="divider"></div>
        <div class="keywords">
            <span>Job Match</span>
            <span>Resume Parsing</span>
            <span>Skill Gaps</span>
            <span>Courses</span>
        </div>
        <div class="info-box">
            Discover the right career path based on your skills and resume
        </div>
        <div class="cta-box">
            <a href="#career-form" class="cta-link">
                <i class="fa-solid fa-arrow-down"></i>
                Start by entering your skills
            </a>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True
)

# ================= FORM =================
st.markdown('<div id="career-form" class="form-section">', unsafe_allow_html=True)

st.markdown("## 🔍 Find Your Best Career Match")

with st.form("career_form"):
    skills = st.text_input("Your Skills", placeholder="e.g. python, sql, data analysis")
    experience = st.text_input("Your Experience", placeholder="e.g. 2 years")
    resume = st.file_uploader(
        "Upload Resume (optional)",
        type=["pdf", "docx"],
        help="Uploading a resume improves match accuracy"
    )
    submit = st.form_submit_button("✨ Get Career Recommendations")

st.markdown("</div></div>", unsafe_allow_html=True)

if submit:
    if not skills.strip() and resume is None:
        st.error("Please enter your skills or upload a resume.")
        st.stop()
    combined_profile=""
    if skills.strip():
        combined_profile+=f"{skills}"
    if experience.strip():
        combined_profile +=f"{experience}"
    if resume is not None:
        resume_text=extractResumeText(resume)
        combined_profile+=f"{resume_text}"
    combined_profile=combined_profile.strip()
    status=st.empty()
    status.chat_message("assistant").write("🔍 Analyzing current job market in Pakistan for your profile...")
    results=analyze_jobs(combined_profile)
    status.empty()

    if not results:
        st.chat_message("assistant").write("❌ No relevant jobs found for your profile at the moment.")
        st.stop()
    st.chat_message("assistant").write(f"📌 Found **{len(results)}** matching jobs:"
    )
    well_matched_count = 0
    not_well_matched_count = 0
    for job in results:
        if job["match_level"] == "Perfect":
            well_matched_count += 1
        else:
            not_well_matched_count += 1



    # ---------- PRE-CALCULATE MATCH COUNTS ----------
  

   

    # ---------- MATCH SUMMARY ----------
    st.subheader("📊 Match Summary")
    st.success(f"✅ Well matched jobs: {well_matched_count}")
    st.warning(f"⚠️ Not well matched jobs: {not_well_matched_count}")

    # ---------- JOB CARDS ----------
    for i in range(0, len(results), 2):
        cols = st.columns(2)

        for col, res in zip(cols, results[i:i + 2]):
            with col:

                st.markdown(
                    f"""
                    <div style="
                        background-color: LightSeaGreen;
                        padding: 18px;
                        border-radius: 18px;
                        margin-bottom: 8px;
                    ">
                        <h3>👨‍💼 {res['job']}</h3>
                        <p><b>Portal:</b> {res.get('portal', 'Job Portal')}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if res["match_level"] == "Perfect":
                    st.success("✅ Perfect Match")
                else:
                    st.warning("🟡 Partial / Not Well Matched")

                portal = res.get("portal", "").lower()

                if "linkedin" in portal:
                    apply_link = "https://www.linkedin.com/jobs/" 
                elif "rozee" in portal:
                    apply_link = "https://www.rozee.pk/"
                else:
                    apply_link = "https://www.google.com/search?q=jobs+in+pakistan"

                st.link_button("Apply Now", apply_link)

                if res["match_level"] != "Perfect":
                    with st.expander("🔎 Why not a good match?"):
                        if res["missing_skills"]:
                            st.markdown(f"**Missing skills:** {', '.join(res['missing_skills'])}" )
                        else:
                            st.markdown("**Missing skills:** None explicitly listed")

                        resources = recommend_resources(res["missing_skills"])
                        if resources:
                            st.markdown("🎓 **Recommended learning:**")
                            for r in resources:
                                st.markdown(f"- {r}")

    st.chat_message("assistant").write(
        "💡 Tip: Improve missing skills or gain experience to increase your match score."
    )
st.markdown("""
<div class="footer">
    © 2026 All rights reserved
</div>
""", unsafe_allow_html=True)



