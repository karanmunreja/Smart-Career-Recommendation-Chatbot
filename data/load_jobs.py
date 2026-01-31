import os
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def load_all_jobs():
    dfs = []

    # ---------- DATASET 1: LinkedIn DS Jobs ----------
    df1 = pd.read_csv(os.path.join(BASE_DIR, "data", "linkedin_ds_jobs.csv"))
    df1["portal"] = "LinkedIn"
    df1["experience"] = ""
    dfs.append(df1[["job_title", "description", "experience", "skills", "portal"]])

    # ---------- DATASET 2: Banking & Finance ----------
    df2 = pd.read_csv(os.path.join(BASE_DIR, "data", "banking_finance_jobs.csv"))
    df2 = df2.rename(columns={
        "Job": "job_title"})
    df2["experience"] = df2.get("Experience", "")
    df2["description"] = ""
    df2["skills"] = ""
    df2["portal"] = "Rozee.pk"
    dfs.append(df2[["job_title", "description", "experience", "skills", "portal"]])

    # ---------- DATASET 3: Pakistan Jobs ----------
    df3 = pd.read_csv(os.path.join(BASE_DIR, "data", "pakistan_jobs.csv"))
    df3['job_title'] = df3.get('jobTitle')
    df3["description"] = ""
    df3["experience"]  = ""
    df3["portal"]      = "LinkedIn"

    dfs.append(df3[["job_title", "description", "experience", "skills", "portal"]])
    # ---------- COMBINE ----------
    df = pd.concat(dfs, ignore_index=True)

    # ---------- CLEAN ----------
    for col in ["job_title", "description", "experience", "skills"]:
        df[col] = df[col].fillna("")

    return df
