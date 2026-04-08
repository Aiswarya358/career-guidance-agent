from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import parse_resume
from agent import run_agent
import uvicorn

app = FastAPI(title="AI Career Guidance Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Career Guidance Agent is running! 🚀"}


@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    """
    Upload a PDF resume and get:
    - Extracted skills
    - Matching job listings
    - Personalized cover letter
    """
    try:
        print(f"📄 Received resume: {file.filename}")
        
        file_bytes = await file.read()
        resume_text = parse_resume(file_bytes)
        
        if not resume_text or len(resume_text) < 10:
            return {
                "success": False,
                "error": "Could not extract text from PDF. Please upload a proper resume."
            }
        print(f"Resume text length: {len(resume_text)}")
        print(f"Resume preview: {resume_text[:200]}")
        
        print("🤖 Running AI agent...")
        result = run_agent(resume_text)
        
        return {
            "success": True,
            "candidate_name": result.get("candidate_name", "Unknown"),
            "job_role": result.get("job_role", "Unknown"),
            "skills": result.get("skills", ""),
            "job_listings": result.get("job_listings", []),
            "cover_letter": result.get("cover_letter", "")
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Backend is running!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)