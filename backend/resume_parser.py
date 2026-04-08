import PyPDF2
import io

def parse_resume(file_bytes: bytes) -> str:
    """Extract text from PDF resume"""
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error parsing resume: {str(e)}"


def extract_skills_prompt(resume_text: str) -> str:
    """Create a prompt to extract skills from resume text"""
    return f"""
You are a professional resume analyzer.
Analyze the following resume and extract:
1. Name of the candidate
2. Key technical skills
3. Soft skills
4. Years of experience
5. Education background
6. Job roles they are suitable for

Resume:
{resume_text}

Respond in a clean structured format.
"""