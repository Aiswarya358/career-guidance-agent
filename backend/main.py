from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from resume_parser import parse_resume
from agent import run_agent
import os

app = FastAPI(title="AI Career Guidance Agent")

# CORS (for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route
@app.get("/")
def home():
    return {"message": "AI Career Guidance Agent is running 🚀"}

# ✅ Health check
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# ✅ Resume analysis endpoint
@app.post("/analyze-resume")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        print(f"📄 Received resume: {file.filename}")

        file_bytes = await file.read()
        resume_text = parse_resume(file_bytes)

        if not resume_text or len(resume_text) < 10:
            return {
                "success": False,
                "error": "Could not extract text from PDF"
            }

        print(f"Resume length: {len(resume_text)}")

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
        print("ERROR:", str(e))
        return {
            "success": False,
            "error": str(e)
        }


# ❌ REMOVE THIS IN PRODUCTION (Render handles it)
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)