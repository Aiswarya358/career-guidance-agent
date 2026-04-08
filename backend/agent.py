from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

# Load env
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key[:10] if api_key else 'NOT FOUND'}")

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)

# -------------------------------
# STEP 1: Extract structured data
# -------------------------------
def extract_data(resume_text: str) -> dict:
    print("🔍 Extracting structured data...")

    messages = [
        SystemMessage(content="You are a strict JSON generator."),
        HumanMessage(content=f"""
Analyze this resume and return ONLY valid JSON.

Format:
{{
  "candidate_name": "string",
  "job_role": "string",
  "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "experience": "string"
}}

Resume:
{resume_text}

IMPORTANT:
- Return ONLY JSON
- No explanation
""")
    ]

    response = llm.invoke(messages)

    try:
        data = json.loads(response.content)
        print("✅ Structured data extracted")
        return data
    except:
        print("❌ JSON parsing failed, fallback used")
        return {
            "candidate_name": "Candidate",
            "job_role": "Software Engineer",
            "skills": ["Python"],
            "experience": "0 years"
        }

# -------------------------------
# STEP 2: Generate structured jobs
# -------------------------------
def find_jobs(skills: list, role: str) -> list:
    print("🔎 Generating job listings...")

    messages = [
        SystemMessage(content="You are a job generator that outputs JSON only."),
        HumanMessage(content=f"""
Based on these skills and role, generate 5 jobs in India.

Skills: {skills}
Role: {role}

Return ONLY JSON:

[
  {{
    "company": "string",
    "role": "string",
    "location": "string"
  }}
]

No explanation.
""")
    ]

    response = llm.invoke(messages)

    try:
        jobs = json.loads(response.content)
        print("✅ Jobs generated")
        return jobs
    except:
        print("❌ Job parsing failed")
        return []

# -------------------------------
# STEP 3: Generate cover letter
# -------------------------------
def generate_cover_letter(skills: list, role: str, name: str) -> str:
    print("✍️ Generating cover letter...")

    messages = [
        SystemMessage(content="You write professional cover letters."),
        HumanMessage(content=f"""
Write a professional cover letter.

Name: {name}
Role: {role}
Skills: {skills}

Keep it clean, 3 paragraphs.
""")
    ]

    response = llm.invoke(messages)
    print("✅ Cover letter generated")
    return response.content

# -------------------------------
# MAIN PIPELINE
# -------------------------------
def run_agent(resume_text: str) -> dict:
    try:
        # Step 1
        data = extract_data(resume_text)

        # Step 2
        jobs = find_jobs(data["skills"], data["job_role"])

        # Step 3
        cover_letter = generate_cover_letter(
            data["skills"],
            data["job_role"],
            data["candidate_name"]
        )

        return {
            "candidate_name": data["candidate_name"],
            "job_role": data["job_role"],
            "skills": data["skills"],  # ✅ now list
            "job_listings": jobs,      # ✅ structured list
            "cover_letter": cover_letter
        }

    except Exception as e:
        print(f"❌ Error in agent: {str(e)}")
        raise e