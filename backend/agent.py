from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os
import json

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

print(f"✅ API Key loaded: {api_key[:10]}...")

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)

# -------------------------------
# STEP 1: EXTRACT DATA (STRICT JSON)
# -------------------------------
def extract_data(resume_text: str) -> dict:
    print("🔍 Extracting structured data...")

    messages = [
        SystemMessage(content="You ONLY return valid JSON. No explanation."),
        HumanMessage(content=f"""
You MUST return valid JSON.

STRICT FORMAT:
{{
  "candidate_name": "string",
  "job_role": "string",
  "skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "experience": "string"
}}

RULES:
- No text before or after JSON
- No markdown
- No explanation

Resume:
{resume_text}
""")
    ]

    response = llm.invoke(messages)

    print("🔴 RAW LLM OUTPUT:\n", response.content)

    try:
        data = json.loads(response.content)
        print("✅ JSON parsed successfully")
        return data

    except Exception as e:
        print("❌ JSON parsing failed:", str(e))

        # fallback (DON'T REMOVE)
        return {
            "candidate_name": "Candidate",
            "job_role": "Software Engineer",
            "skills": ["Python"],
            "experience": "0 years"
        }

# -------------------------------
# STEP 2: JOB GENERATION (JSON)
# -------------------------------
def find_jobs(skills: list, role: str) -> list:
    print("🔎 Generating job listings...")

    messages = [
        SystemMessage(content="Return ONLY JSON."),
        HumanMessage(content=f"""
Generate 5 job listings in India.

Skills: {skills}
Role: {role}

STRICT FORMAT:

[
  {{
    "company": "string",
    "role": "string",
    "location": "string"
  }}
]

RULES:
- Only JSON
- No explanation
""")
    ]

    response = llm.invoke(messages)

    print("🔴 RAW JOB OUTPUT:\n", response.content)

    try:
        jobs = json.loads(response.content)
        print("✅ Jobs parsed successfully")
        return jobs

    except Exception as e:
        print("❌ Job parsing failed:", str(e))
        return []

# -------------------------------
# STEP 3: COVER LETTER
# -------------------------------
def generate_cover_letter(skills: list, role: str, name: str) -> str:
    print("✍️ Generating cover letter...")

    messages = [
        SystemMessage(content="Write a professional cover letter."),
        HumanMessage(content=f"""
Write a clean professional cover letter.

Name: {name}
Role: {role}
Skills: {skills}

3 paragraphs:
1. Intro
2. Skills
3. Closing
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
        # STEP 1
        data = extract_data(resume_text)

        # STEP 2
        jobs = find_jobs(data["skills"], data["job_role"])

        # STEP 3
        cover_letter = generate_cover_letter(
            data["skills"],
            data["job_role"],
            data["candidate_name"]
        )

        return {
            "candidate_name": data["candidate_name"],
            "job_role": data["job_role"],
            "skills": data["skills"],
            "job_listings": jobs,
            "cover_letter": cover_letter
        }

    except Exception as e:
        print(f"❌ Error in agent: {str(e)}")
        raise e