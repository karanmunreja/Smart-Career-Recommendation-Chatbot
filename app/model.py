import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scraper import scrape_jobs


# ---------- DOMAIN DETECTION ----------
def detect_domain(user_input):
    text = user_input.lower()

    if "fashion" in text:
        return "fashion"
    elif "design" in text:
        return "design"
    elif "marketing" in text:
        return "marketing"
    elif "business" in text:
        return "business"
    elif "python" in text or "software" in text:
        return "tech"
    else:
        return "general"


# ---------- LOAD & MERGE DATA ----------
def load_data(user_input):
    domain = detect_domain(user_input)

    # Load static dataset and tag it
    df_static = pd.read_csv("/data/jobs.csv")
    df_static["portal"] = "Local Dataset"
    df_static["apply_link"] = "https://pk.indeed.com"

    # Load scraped jobs
    try:
        df_scraped = scrape_jobs(domain)
        df = pd.concat([df_scraped, df_static], ignore_index=True)
    except:
        df = df_static

    return df



def skill_gap_analysis(user_skills, job_skills):
    user_set = set(user_skills.replace(",", " ").lower().split())
    job_set = set(job_skills.replace(",", " ").lower().split())
    return list(job_set - user_set)

def analyze_jobs(user_input):
    df = load_data(user_input)
    df["text"] = df["job_title"] + " " + df["skills_required"]

    vectorizer = TfidfVectorizer()
    job_vectors = vectorizer.fit_transform(df["text"])

    user_vector = vectorizer.transform([user_input])
    similarities = cosine_similarity(user_vector, job_vectors)[0]

    results = []

    for idx, score in enumerate(similarities):
        if score > 0.2:  # relevance threshold
            missing = skill_gap_analysis(
                user_input,
                df.iloc[idx]["skills_required"]
            )

            results.append({
                "job": df.iloc[idx]["job_title"],
                "portal": df.iloc[idx].get("portal", "Indeed Pakistan"),
                "apply_link": df.iloc[idx].get("apply_link", "https://pk.indeed.com"),
                "missing_skills": missing
            })

    return results


# ---------- TRUSTED LEARNING RESOURCES ----------
TRUSTED_RESOURCES = {
    "python": "Coursera – Python for Everybody",
    "sql": "Coursera – SQL for Data Science",
    "statistics": "Coursera – Statistics for Data Science",
    "excel": "Coursera – Excel Skills for Business",
    "fashion": "Coursera – Fashion Design",
    "design": "Google UX Design Certificate",
    "marketing": "Google Digital Marketing Certificate",
    "seo": "Coursera – SEO Specialization",
    "communication": "Coursera – Communication Skills"
}


def recommend_resources(missing_skills):
    resources = []
    for skill in missing_skills:
        if skill in TRUSTED_RESOURCES:
            resources.append(TRUSTED_RESOURCES[skill])
    return list(set(resources))
