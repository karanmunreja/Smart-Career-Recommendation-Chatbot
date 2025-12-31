import streamlit as st
from model import analyze_jobs, recommend_resources

st.set_page_config(page_title="Career Recommendation Chatbot")

st.title("🎓 Smart Career Recommendation Chatbot")
st.write("Fill the form below to see current job opportunities in Pakistan based on your profile.")

# ---------- FORM ----------
with st.form("career_form"):
    education = st.selectbox(
        "Your Education",
        ["BS CS", "BS IT", "BS SE", "Other"]
    )
    skills = st.text_input("Your Skills (comma or space separated)")
    interests = st.text_input("Your Interests")
    submitted = st.form_submit_button("Get Job Recommendations")

# ---------- CHATBOT RESPONSE ----------
if submitted:
    user_profile = skills + " " + interests

    # Placeholder for analyzing message
    status_placeholder = st.empty()
    status_placeholder.chat_message("assistant").write(
        "🔍 Analyzing current job market in Pakistan for your profile..."
    )

    # Analyze jobs
    results = analyze_jobs(user_profile)

    # Remove analyzing message
    status_placeholder.empty()

    if not results:
        st.chat_message("assistant").write(
            "❌ No relevant jobs found for your profile at the moment."
        )
    else:
        st.chat_message("assistant").write(
            "📌 Here are some **current jobs matching your profile:**"
        )

        # ---------- JOB CARDS (2 per row) ----------
        for i in range(0, len(results), 2):
            cols = st.columns(2)

            for col, res in zip(cols, results[i:i+2]):
                with col:
                    st.markdown(
                        f"""
                        <div style="
                            border: 1px solid #444;
                            border-radius: 12px;
                            padding: 15px;
                            margin-bottom: 15px;
                            background-color: #111;
                        ">
                            <h4>👨‍💼 {res['job']}</h4>
                            <p><b>Portal:</b> {res.get('portal', 'Indeed Pakistan')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.link_button(
                        "Apply Now",
                        res.get("apply_link", "https://pk.indeed.com")
                    )

                    if res["missing_skills"]:
                        st.caption(
                            f"❌ Missing skills: {', '.join(res['missing_skills'])}"
                        )

                        resources = recommend_resources(res["missing_skills"])
                        if resources:
                            st.caption(
                                "🎓 Learn from:\n- " + "\n- ".join(resources)
                            )
                    else:
                        st.caption("✅ You already match this job well!")

        # ---------- CHATBOT SUGGESTION ----------
        st.chat_message("assistant").write(
            "💡 Tip: Focus on improving the missing skills to increase your chances. "
            "Would you like a **learning roadmap** or **resume tips**?"
        )
