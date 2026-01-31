import sys
import os
import re

# ================= PATH FIX =================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.load_jobs import load_all_jobs


# ================= SKILLS =================

SKILLS = [
    # Tech
    "python", "sql", "java", "c++", "javascript",
    "react", "node", "angular", "vue", "express",
    "django", "flask", "fastapi",

    # Data
    "machine learning", "deep learning", "artificial intelligence",
    "data analysis", "data science", "data visualization",
    "power bi", "tableau", "excel",
    "pandas", "numpy", "scikit-learn",

    # Databases
    "mysql", "postgresql", "mongodb", "firebase",

    # Cloud / DevOps
    "aws", "azure", "gcp",
    "docker", "kubernetes",
    "ci/cd", "git", "github",

    # QA / Testing
    "testing", "qa", "automation testing",
    "selenium", "unit testing",

    # Business / ERP
    "business analysis", "analytics",
    "finance", "accounting", "banking",
    "erp", "sap", "crm",

    # Marketing
    "seo", "digital marketing", "content marketing",
    "social media marketing", "email marketing"
]


# ================= SCORE THRESHOLDS =================
PERFECT_SCORE_THRESHOLD = 0.35
PARTIAL_SCORE_THRESHOLD = 0.25


# ================= UTIL FUNCTIONS =================

def extract_skills(text):
    text = str(text).lower()
    return [s for s in SKILLS if s in text]


def convert_to_years(text):
    text = text.lower()

    m = re.search(r"(\d+(\.\d+)?)\s*month", text)
    if m:
        return float(m.group(1)) / 12

    y = re.search(r"(\d+(\.\d+)?)\s*year", text)
    if y:
        return float(y.group(1))

    return 0.0


def infer_job_experience(text):
    text = text.lower()

    m = re.search(r"(\d+(\.\d+)?)\+?\s*year", text)
    if m:
        return float(m.group(1))

    if "intern" in text:
        return 0
    if "junior" in text:
        return 1
    if "mid" in text:
        return 3
    if "senior" in text or "lead" in text:
        return 5

    return None


def experience_match_score(user_exp, job_exp):
    if job_exp is None:
        return 0.8
    if user_exp >= job_exp:
        return 1.0
    if user_exp >= job_exp * 0.7:
        return 0.5
    return 0.0


# ================= JOB SKILL HANDLING =================

def get_job_skills(row):
    """
    Skills specified if:
    - Explicit skills column OR
    - Inferred from job title + description
    """
    explicit = extract_skills(row.get("skills", ""))
    if explicit:
        return set(explicit), "explicit"

    inferred = extract_skills(
        row.get("job_title", "") + " " + row.get("description", "")
    )
    if inferred:
        return set(inferred), "inferred"

    return set(), "none"


# ================= MAIN ENGINE =================

def analyze_jobs(user_input):
    df = load_all_jobs()
    if df.empty:
        return []

    user_skills = extract_skills(user_input)
    user_skill_set = set(user_skills)
    user_exp = convert_to_years(user_input)

    if not user_skills and user_exp == 0:
        return []

    # Clean job data
    df["job_title"] = df["job_title"].fillna("")
    df["description"] = df["description"].fillna("")
    df["skills"] = df.get("skills", "").fillna("")

    df["combined_text"] = df["job_title"] + " " + df["description"]

    # TF-IDF
    vectorizer = TfidfVectorizer(stop_words="english")
    job_vectors = vectorizer.fit_transform(df["combined_text"])
    user_vector = vectorizer.transform([user_input])

    semantic_scores = cosine_similarity(user_vector, job_vectors)[0]

    results = []

    for idx, row in df.iterrows():

        job_skills, skills_source = get_job_skills(row)
        skills_specified = skills_source in ["explicit", "inferred"]

        # Skill score
        if job_skills:
            skill_score = len(user_skill_set & job_skills) / len(job_skills)
        else:
            skill_score = 0.7

        # Experience score
        job_exp = infer_job_experience(row["combined_text"])
        exp_score = experience_match_score(user_exp, job_exp)

        # Final score (ranking + decision)
        final_score = (
            0.5 * semantic_scores[idx] +
            0.3 * skill_score +
            0.2 * exp_score
        )

        # ================= MATCH DECISION =================

        # CASE 1: Skills specified → skill-based
        if skills_specified:
            missing_skills = list(job_skills - user_skill_set)

            if len(missing_skills) == 0:
                match_level = "Perfect"
            else:
                match_level = "Partial"

        # CASE 2: Skills NOT specified → score-based (3-level)
        else:
            missing_skills = ["Not explicitly listed"]

            if final_score >= PERFECT_SCORE_THRESHOLD:
                match_level = "Perfect"
            elif final_score >= PARTIAL_SCORE_THRESHOLD:
                match_level = "Partial"
            else:
                continue  # ❌ filtered out

        # ==================================================

        results.append({
            "job": row["job_title"],
            "portal": row.get("portal", "Job Portal"),
            "apply_link": row.get("apply_link", ""),
            "job_skills": list(job_skills),
            "missing_skills": missing_skills,
            "skills_source": skills_source,
            "match_score": round(final_score, 3),
            "match_level": match_level
        })

    # Sort: Perfect first, then by score
    results.sort(
        key=lambda r: (r["match_level"] != "Perfect", -r["match_score"])
    )

    return results


# ================= COURSE RECOMMENDATION =================

TRUSTED_RESOURCES = {
    "python": "Coursera – Python for Everybody",
    "sql": "Coursera – SQL for Data Science",
    "excel": "Coursera – Excel Skills for Business",
    "machine learning": "Andrew Ng – Machine Learning",
    "seo": "Coursera – SEO Specialization"
}


def recommend_resources(missing_skills):
    return list(
        {TRUSTED_RESOURCES[s] for s in missing_skills if s in TRUSTED_RESOURCES}
    )
