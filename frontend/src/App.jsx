import { useState } from "react";
import axios from "axios";

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [emailStatus, setEmailStatus] = useState("");
  const [selectedJob, setSelectedJob] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Please upload a PDF resume first!");
      return;
    }
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const response = await axios.post(
        "http://localhost:8000/analyze-resume",
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      setResult(response.data);
    } catch (err) {
      setError("Something went wrong! Make sure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (result?.cover_letter) {
      const textarea = document.createElement("textarea");
      textarea.value = result.cover_letter;
      document.body.appendChild(textarea);
      textarea.select();
      document.execCommand("copy");
      document.body.removeChild(textarea);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleSendEmail = (job) => {
    const subject = `Application for ${result?.job_role} Position`;
    const body = result?.cover_letter || "";
    
    // This creates a direct link to Gmail compose page
    const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&to=${job.email}&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    
    window.open(gmailUrl, "_blank");
  };

  const parseJob = (jobText) => {
    const lines = jobText.split('\n').filter(l => l.trim());
    let company = "", title = "", email = "", location = "";
    for (const line of lines) {
      if (line.includes("Company")) company = line.split(':')[1]?.trim() || "";
      if (line.includes("Job Title")) title = line.split(':')[1]?.trim() || "";
      if (line.includes("Email")) email = line.split(':')[1]?.trim() || "";
      if (line.includes("Location")) location = line.split(':')[1]?.trim() || "";
    }
    return { company, title, email, location, full: jobText };
  };

  return (
    <div style={{
      minHeight: "100vh",
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      fontFamily: "Arial, sans-serif",
      padding: "30px 20px"
    }}>

      {/* Header */}
      <div style={{ textAlign: "center", color: "white", marginBottom: "30px" }}>
        <h1 style={{ fontSize: "2rem", margin: 0 }}>🤖 AI Career Guidance Agent</h1>
        <p style={{ opacity: 0.85, marginTop: "8px" }}>
          Upload your resume → AI finds jobs + writes your cover letter
        </p>
      </div>

      {/* Upload Card */}
      <div style={{
        maxWidth: "650px", margin: "0 auto", background: "white",
        borderRadius: "16px", padding: "30px",
        boxShadow: "0 20px 60px rgba(0,0,0,0.3)"
      }}>
        <h2 style={{ color: "#333", marginTop: 0 }}>📄 Upload Resume (PDF)</h2>

        <div style={{
          border: "2px dashed #667eea", borderRadius: "12px",
          padding: "25px", textAlign: "center", background: "#f8f7ff",
          cursor: "pointer", marginBottom: "20px"
        }}>
          <input type="file" accept=".pdf" onChange={handleFileChange}
            style={{ display: "none" }} id="fileInput" />
          <label htmlFor="fileInput" style={{ cursor: "pointer" }}>
            <div style={{ fontSize: "2.5rem" }}>📁</div>
            <p style={{ color: "#667eea", fontWeight: "bold", margin: "8px 0 4px" }}>
              Click to upload PDF
            </p>
          </label>
          {file && (
            <div style={{
              marginTop: "10px", padding: "8px 12px",
              background: "#e8f5e9", borderRadius: "8px", color: "#2e7d32"
            }}>
              ✅ {file.name}
            </div>
          )}
        </div>

        <button onClick={handleSubmit} disabled={loading} style={{
          width: "100%", padding: "14px",
          background: loading ? "#ccc" : "linear-gradient(135deg, #667eea, #764ba2)",
          color: "white", border: "none", borderRadius: "10px",
          fontSize: "1rem", fontWeight: "bold",
          cursor: loading ? "not-allowed" : "pointer"
        }}>
          {loading ? "⏳ AI is analyzing your resume..." : "🚀 Analyze My Resume"}
        </button>

        {error && (
          <div style={{
            marginTop: "12px", padding: "12px",
            background: "#ffebee", borderRadius: "8px", color: "#c62828"
          }}>❌ {error}</div>
        )}
      </div>

      {/* Results */}
      {result?.success && (
        <div style={{ maxWidth: "650px", margin: "20px auto" }}>

          {/* Profile Card */}
          <div style={{
            background: "white", borderRadius: "16px", padding: "25px",
            marginBottom: "20px", boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
          }}>
            <h2 style={{ color: "#333", marginTop: 0 }}>👤 Candidate Profile</h2>
            <p style={{ margin: "6px 0" }}>
              <strong>Name:</strong> {result.candidate_name}
            </p>
            <p style={{ margin: "6px 0" }}>
              <strong>Best Role:</strong> {result.job_role}
            </p>
            <p style={{ margin: "6px 0" }}>
              <strong>Skills:</strong> {result.skills?.split('\n')
                .find(l => l.startsWith('Skills:'))?.replace('Skills:', '').trim()}
            </p>
          </div>

          {/* Job Listings */}
          <div style={{
            background: "white", borderRadius: "16px", padding: "25px",
            marginBottom: "20px", boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
          }}>
            <h2 style={{ color: "#333", marginTop: 0 }}>💼 Matching Jobs</h2>
            <p style={{ color: "#666", fontSize: "0.9rem", marginTop: "-10px" }}>
              Click "Apply via Email" to send your cover letter directly!
            </p>

            {result.job_listings.map((job, index) => {
              const parsed = parseJob(job);
              return (
                <div key={index} style={{
                  padding: "15px", background: "#f8f7ff",
                  borderRadius: "10px", marginBottom: "12px",
                  borderLeft: "4px solid #667eea"
                }}>
                  <p style={{ margin: "4px 0", fontWeight: "bold", color: "#333" }}>
                    🏢 {parsed.company} — {parsed.title}
                  </p>
                  <p style={{ margin: "4px 0", color: "#555", fontSize: "0.9rem" }}>
                    📍 {parsed.location}
                  </p>
                  <p style={{ margin: "4px 0", color: "#555", fontSize: "0.9rem" }}>
                    📧 {parsed.email}
                  </p>
                  <button
                    onClick={() => handleSendEmail(parsed)}
                    style={{
                      marginTop: "10px", padding: "8px 16px",
                      background: "#667eea", color: "white",
                      border: "none", borderRadius: "6px",
                      cursor: "pointer", fontWeight: "bold", fontSize: "0.9rem"
                    }}>
                    📨 Apply via Email
                  </button>
                </div>
              );
            })}
          </div>

          {/* Cover Letter */}
          <div style={{
            background: "white", borderRadius: "16px", padding: "25px",
            marginBottom: "20px", boxShadow: "0 10px 30px rgba(0,0,0,0.2)"
          }}>
            <h2 style={{ color: "#333", marginTop: 0 }}>✍️ Your Cover Letter</h2>
            <div style={{
              padding: "20px", background: "#f8f7ff", borderRadius: "8px",
              whiteSpace: "pre-wrap", lineHeight: "1.8",
              fontSize: "0.95rem", color: "#333", marginBottom: "15px"
            }}>
              {result.cover_letter}
            </div>
            <button onClick={handleCopy} style={{
              padding: "10px 24px",
              background: copied ? "#4caf50" : "#667eea",
              color: "white", border: "none", borderRadius: "8px",
              cursor: "pointer", fontWeight: "bold", fontSize: "0.95rem"
            }}>
              {copied ? "✅ Copied!" : "📋 Copy Cover Letter"}
            </button>
          </div>

        </div>
      )}
    </div>
  );
}