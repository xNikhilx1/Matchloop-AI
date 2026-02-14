# MatchLoop AI - Backend

This is the Python Flask backend for the MatchLoop AI application.

## Features

- Job position management (CRUD operations)
- Resume file upload and processing (PDF, DOCX, DOC)
- Text extraction from various document formats
- AI-powered resume analysis using Gemma AI
- SQLite database for data persistence
- RESTful API endpoints

## Setup Instructions

### 1. Create Virtual Environment

```bash
# Navigate to backend folder
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Edit the `config.env` file and add your Google AI API key (get it from [Google AI Studio](https://aistudio.google.com/)):

```env
GEMMA_API_KEY=your_google_ai_api_key_here
GEMMA_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent
FLASK_ENV=development
FLASK_DEBUG=1
```

### 4. Run the Application

```bash
python app.py
```

The backend will start on `http://localhost:5000`

## API Endpoints

### Health Check
- `GET /api/health` - Check if the backend is running

### Job Management
- `GET /api/jobs` - Get all job positions
- `POST /api/jobs` - Create a new job position
- `GET /api/jobs/<id>` - Get a specific job position

### Resume Management
- `POST /api/upload-resume` - Upload a resume file
- `POST /api/analyze-resume` - Analyze resume compatibility with a job

## Database Schema

The application uses SQLite with the following table:

```sql
CREATE TABLE job_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position_name TEXT NOT NULL,
    job_description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## File Upload

- Supported formats: PDF, DOCX, DOC
- Maximum file size: 16MB
- Files are stored in the `resumeupload` folder
- All files are renamed to `resume_1.{extension}`

## AI Integration

The application uses Google's Generative AI API (Gemma 3 27B model) for resume analysis. Make sure to:
1. Get a valid API key from [Google AI Studio](https://aistudio.google.com/)
2. Configure the API key in `config.env`
3. Ensure internet connectivity for API calls
4. The application includes a fallback analysis system if AI services are unavailable
5. Uses Google's official `google-generativeai` Python client for reliable API communication

## Error Handling

The application includes comprehensive error handling for:
- File upload issues
- Database errors
- API failures
- Invalid file formats
- Missing dependencies

## Development

- Debug mode is enabled by default
- CORS is enabled for frontend integration
- Logs are printed to console
- Database is automatically initialized on startup
