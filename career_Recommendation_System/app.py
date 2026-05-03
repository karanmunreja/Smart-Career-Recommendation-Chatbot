# ============================================================
# CareerLens - Smart Career Recommendation Chatbot
# ============================================================
# Copyright (c) 2026 Karan Munreja. All rights reserved.
#
# PROPRIETARY AND CONFIDENTIAL
# This software and all associated documentation are proprietary to Karan Munreja.
# Unauthorized copying, distribution, modification, or reuse of this software,
# in whole or in part, is strictly prohibited without explicit written permission
# from the copyright holder.
#
# NO LICENSE GRANTED - NO REUSE PERMITTED
# This code is provided as-is for personal use only.
# Any commercial use, reproduction, or redistribution is forbidden.
#
# Project Repository: https://github.com/karanmunreja/Smart-Career-Recommendation-Chatbot
# Author: Karan Munreja
# Created: 2026
# ============================================================
# Description:
# This module implements the main Streamlit web interface for CareerLens,
# a career recommendation system that matches user profiles with job opportunities
# in the Pakistan job market and suggests learning resources for skill gaps.
# ============================================================

import streamlit as st
from utils import extractResumeText
from model import analyze_jobs,recommend_resources

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="CareerLens",
    layout="wide"
)

tHEME_COLOR = "#3F3DE0"

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
    color: {{THEME_COLOR}};
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
    background: linear-gradient(90deg, {{THEME_COLOR}}, #8B8AF8);
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
    color: {{THEME_COLOR}};
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
    background: linear-gradient(90deg, {{THEME_COLOR}}, #6366F1) !important;
    color: white !important;
    border: none !important;
}}
</style>
""",
    unsafe_allow_html=True
)