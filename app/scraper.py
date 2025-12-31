import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_jobs(domain="general"):
    base_url = "https://pk.indeed.com/jobs?q="

    domain_queries = {
        "tech": "software+developer",
        "design": "graphic+designer",
        "fashion": "fashion+designer",
        "business": "business+analyst",
        "marketing": "digital+marketing",
        "general": "jobs"
    }

    query = domain_queries.get(domain, "jobs")
    url = base_url + query + "&l=Pakistan"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for job in soup.select("h2.jobTitle")[:6]:  # limit for safety
        title = job.get_text(strip=True)

        # Infer skills from title (academic & realistic)
        if "data" in title.lower():
            skills = "Python, SQL, Statistics, Excel"
        elif "fashion" in title.lower():
            skills = "Fashion Design, Textile, Creativity"
        elif "design" in title.lower():
            skills = "Design, Creativity, Adobe"
        elif "marketing" in title.lower():
            skills = "SEO, Content, Marketing"
        elif "developer" in title.lower():
            skills = "HTML, CSS, JavaScript, Python"
        else:
            skills = "Communication, Problem Solving"

        # Indeed job
        jobs.append({
            "job_title": title,
            "skills_required": skills,
            "education": "Any",
            "portal": "Indeed Pakistan",
            "apply_link": f"https://pk.indeed.com/jobs?q={title.replace(' ', '+')}"
        })

        # LinkedIn job (simulated safely)
        jobs.append({
            "job_title": title,
            "skills_required": skills,
            "education": "Any",
            "portal": "LinkedIn Pakistan",
            "apply_link": f"https://www.linkedin.com/jobs/search/?keywords={title.replace(' ', '%20')}"
        })

    return pd.DataFrame(jobs)
