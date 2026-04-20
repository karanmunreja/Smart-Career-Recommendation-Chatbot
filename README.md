🚀 Smart Career Recommendation System

This is my Data Science semester project, where I built an AI-powered job recommendation system by applying data preprocessing
and machine learning techniques to provide personalized job suggestions and identify skill gaps with course recommendations.

📌 Overview

Finding suitable job opportunities among thousands of listings can be overwhelming. 
This project solves that problem by intelligently matching user profiles with job descriptions using
Natural Language Processing (NLP) techniques.

Instead of manually searching, the system:
Analyzes user input and resume
Matches with job postings
Ranks jobs based on relevance
Identifies missing skills
Suggests learning resources

Screenshots of Workflow:
<img width="1118" height="698" alt="p4" src="https://github.com/user-attachments/assets/d02f78e0-5e31-4cf2-a880-4aef1b22743f" />
<img width="1295" height="809" alt="p2" src="https://github.com/user-attachments/assets/0ccb0d72-dbb1-4ee5-8e9b-eeb88a90f5da" />
<img width="1095" height="684" alt="p3" src="https://github.com/user-attachments/assets/59ab9646-fb78-4d9a-afee-4431a77828d5" />
<img width="1118" height="698" alt="p4" src="https://github.com/user-attachments/assets/02b1d27f-0d48-4e1c-8a07-5158a7ae5799" />


🎯 Key Features
📄 Resume upload (PDF/DOCX) with automatic skill extraction
🧠 Job matching using TF-IDF and cosine similarity
📊 Experience-based filtering
🔍 Perfect vs Partial match classification
❗ Missing skill identification
🎓 Course recommendation system
💻 Interactive UI using Streamlit

- How It Works
🔄 Workflow
User provides: Skills, Experience, Interests, Resume (optional)
System processes: Text preprocessing, TF-IDF vectorization, Cosine similarity
Scoring: Semantic similarity, Skill matching, Experience compatibility
Output:Ranked job recommendations, Match classification, Missing skills, Suggested courses.


🛠️ Tech Stack
🔹 Language
Python
🔹 Libraries
Pandas
NumPy
Scikit-learn
pdfplumber
python-docx
Regular Expressions
🔹 Framework
Streamlit

📊 Algorithms & Techniques
TF-IDF Vectorization
Cosine Similarity
Rule-based Experience Matching
Skill Gap Analysis

💡 Highlights
Hybrid approach (NLP + rule-based logic)
Works with incomplete job data
No heavy ML training required
Practical and scalable system

📂 Dataset
Job postings dataset (CSV) collected from Kaggle
📸 Example Output
“Strong match for Data Analyst role”
“Missing skills: SQL, Power BI”
“Recommended courses: Data Analysis with Python”
⚙️ How to Run the Project (Simple Setup)

Follow these steps to run the project on your system:

🔹 1. Clone or Download Project
git clone https://github.com/your-username/smart-career-recommendation.git
cd smart-career-recommendation
🔹 2. Install Required Libraries
pip install streamlit pandas numpy scikit-learn pdfplumber python-docx
🔹 3. Run the Application
streamlit run app.py
🔹 4. Open in Browser

After running, open:

👉 http://localhost:8501

🔹 5. Use the System
Enter:
Skills, Experience, Interests OR Upload resume (PDF / DOCX)
🎯 Output You Will Get
✅ Job recommendations
✅ Match type (Perfect / Partial)
✅ Missing skills
✅ Course suggestions


⚠️ Limitations
Depends on dataset quality
Keyword-based matching (limited semantic understanding)
Recommendations may require validation

🔮 Future Scope
Use advanced NLP (BERT, embeddings)
Real-time job scraping
Personalized recommendations
Voice-based interaction

🎓 Learning Outcomes
Applied NLP to real-world problem
Built end-to-end recommendation system
Integrated backend and UI
Implemented intelligent ranking system


📌 Conclusion

This project demonstrates how lightweight NLP techniques can be used to build an intelligent and practical career 
recommendation system that helps users make better career decisions.
