import { useState } from "react";
import "./App.css";

function App() {
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const createJob = async () => {
    const res = await fetch("http://127.0.0.1:5000/api/jobs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        position_name: "Software Developer",
        job_description: jobDesc,
      }),
    });
    const data = await res.json();
    return data.job_id;
  };

  const uploadResume = async (file) => {
    const formData = new FormData();
    formData.append("resume", file);

    await fetch("http://127.0.0.1:5000/api/upload-resume", {
      method: "POST",
      body: formData,
    });
  };

  const analyze = async (jobId) => {
    const res = await fetch("http://127.0.0.1:5000/api/analyze-resume", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_id: jobId }),
    });

    const data = await res.json();
    setResult(data.analysis);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const file = e.target.resume.files[0];
    if (!file) return alert("Upload resume");

    setLoading(true);
    const jobId = await createJob();
    await uploadResume(file);
    await analyze(jobId);
    setLoading(false);
  };

  return (
    <div className="page">
      <header className="navbar">
        <div className="logo">MatchLoop AI</div>
      </header>

      <main className="main">
        <section className="left">
          <h1>AI Resume Compatibility Analyzer</h1>
          <p>
            Upload your resume and evaluate how well it matches a job
            description using AI.
          </p>
        </section>

        <section className="right">
          <form onSubmit={handleSubmit}>
            <textarea
              placeholder="Paste Job Description..."
              value={jobDesc}
              onChange={(e) => setJobDesc(e.target.value)}
            />

            <input type="file" name="resume" />

            <button type="submit">
              {loading ? "Analyzing..." : "Analyze Resume"}
            </button>
          </form>

          {result && (
            <div className="result">
              <h2>Score: {result.compatibility_score}</h2>
              <h3>Strengths</h3>
              <ul>
                {result.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
              <h3>Weaknesses</h3>
              <ul>
                {result.weaknesses.map((w, i) => (
                  <li key={i}>{w}</li>
                ))}
              </ul>
              <p>{result.analysis}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
