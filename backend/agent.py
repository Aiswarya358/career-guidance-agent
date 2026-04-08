from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv
import os

load_dotenv(override=True)

api_key = os.getenv("GROQ_API_KEY")
print(f"API Key loaded: {api_key[:10] if api_key else 'NOT FOUND'}")

llm = ChatGroq(
    api_key=api_key,
    model="llama-3.3-70b-versatile"
)


def extract_skills(resume_text: str) -> dict:
    """Step 1 - Extract skills from resume"""
    print("🔍 Extracting skills from resume...")
    
    messages = [
        SystemMessage(content="You are a professional resume analyzer."),
        HumanMessage(content=f"""
Analyze this resume and extract:
1. Candidate full name
2. Top 5 technical skills
3. Years of experience
4. Most suitable job role

Resume:
{resume_text}

Reply in this exact format:
Name: [name]
Skills: [skill1, skill2, skill3, skill4, skill5]
Experience: [X years]
Best Role: [job role]
""")
    ]
    
    response = llm.invoke(messages)
    content = response.content
    
    name = "Candidate"
    role = "Software Developer"
    
    for line in content.split('\n'):
        if line.startswith('Name:'):
            name = line.replace('Name:', '').strip()
        if line.startswith('Best Role:'):
            role = line.replace('Best Role:', '').strip()
    
    print(f"✅ Skills extracted for: {name}")
    return {"skills": content, "candidate_name": name, "job_role": role}


def find_jobs(skills: str, role: str) -> list:
    """Step 2 - Find matching jobs"""
    print("🔎 Finding matching jobs...")
    
    messages = [
        SystemMessage(content="You are a job search expert for the Indian job market."),
        HumanMessage(content=f"""
Based on these skills, suggest 5 job opportunities in India:

{skills}

For each job provide:
- Company Name
- Job Title  
- Required Skills
- HR Email (realistic example)
- Location

Format each job numbered 1-5, separated by blank lines.
""")
    ]
    
    response = llm.invoke(messages)
    jobs = [j for j in response.content.split('\n\n') if j.strip()]
    
    print(f"✅ Found {len(jobs)} job matches!")
    return jobs


def generate_cover_letter(skills: str, role: str, name: str) -> str:
    """Step 3 - Generate cover letter"""
    print("✍️ Generating cover letter...")
    
    messages = [
        SystemMessage(content="You are an expert career coach who writes outstanding cover letters."),
        HumanMessage(content=f"""
Write a professional cover letter for:

Candidate: {name}
Role: {role}
Skills: {skills}

Write 3 paragraphs:
1. Introduction and interest in the role
2. Key skills and achievements
3. Strong closing with call to action
""")
    ]
    
    response = llm.invoke(messages)
    print("✅ Cover letter generated!")
    return response.content


def run_agent(resume_text: str) -> dict:
    """Run the full pipeline"""
    try:
        # Step 1
        skills_data = extract_skills(resume_text)
        
        # Step 2
        jobs = find_jobs(skills_data["skills"], skills_data["job_role"])
        
        # Step 3
        cover_letter = generate_cover_letter(
            skills_data["skills"],
            skills_data["job_role"],
            skills_data["candidate_name"]
        )
        
        return {
            "candidate_name": skills_data["candidate_name"],
            "job_role": skills_data["job_role"],
            "skills": skills_data["skills"],
            "job_listings": jobs,
            "cover_letter": cover_letter
        }
    except Exception as e:
        print(f"❌ Error in agent: {str(e)}")
        raise e