<<<<<<< HEAD
# MatchLoop AI

A comprehensive web application that uses AI to analyze resume compatibility with job descriptions. Built with Python Flask backend and React frontend, designed to provide enterprise-grade recruitment solutions.

## Features

- **Job Position Management**: Create and manage job positions with detailed descriptions
- **Resume Upload**: Support for PDF, DOCX, and DOC files with automatic text extraction
- **AI-Powered Analysis**: Get compatibility scores and detailed analysis using Gemma AI
- **Modern UI**: Beautiful, responsive interface with drag-and-drop file upload
- **Database Storage**: SQLite database for persistent data storage
- **File Management**: Automatic file renaming and storage management

## Project Structure

```
resume_parser_ai/
├── backend/                 # Python Flask backend
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── config.env          # Environment configuration
│   ├── resumeupload/       # Resume file storage
│   └── README.md           # Backend documentation
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── App.js          # Main application
│   │   └── index.js        # Entry point
│   ├── package.json        # Node.js dependencies
│   └── public/             # Static files
└── README.md               # This file
```

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- Gemma AI API key

## Setup Instructions

### Step 1: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   # On Windows:
   python -m venv .venv
   .venv\Scripts\activate
   
   # On macOS/Linux:
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Edit `config.env` file
   - Add your Google AI API key (get it from [Google AI Studio](https://aistudio.google.com/)):
           ```env
      GEMMA_API_KEY=your_google_ai_api_key_here
      GEMMA_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemma-3-27b-it:generateContent
      ```

5. **Run the backend:**
   ```bash
   python app.py
   ```
   
   The backend will start on `http://localhost:5000`

### Step 2: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm start
   ```
   
   The frontend will start on `http://localhost:3000`

## Usage

### 1. Add Job Positions
- Navigate to "Add Job Position"
- Enter position name and detailed job description
- Click "Create Job Position"

### 2. Upload Resume
- Go to "Upload Resume" section
- Drag and drop or click to browse
- Supported formats: PDF, DOCX, DOC
- Maximum file size: 16MB
- File will be renamed to "resume_1" and stored

### 3. Analyze Resume
- Navigate to "Analyze Resume"
- Select a job position from the dropdown
- Click "Analyze Resume"
- View AI-generated compatibility score and analysis

### 4. View Results
- Compatibility score (0-100%)
- Strengths that match job requirements
- Areas for improvement
- Detailed analysis and recommendations
- Resume text preview

## API Endpoints

### Backend API (http://localhost:5000)

- `GET /api/health` - Health check
- `GET /api/jobs` - Get all job positions
- `POST /api/jobs` - Create new job position
- `GET /api/jobs/<id>` - Get specific job position
- `POST /api/upload-resume` - Upload resume file
- `POST /api/analyze-resume` - Analyze resume compatibility

## Configuration

### Environment Variables (backend/config.env)
- `GEMMA_API_KEY`: Your Google AI API key (from Google AI Studio)
- `GEMMA_API_URL`: Google Generative AI API endpoint for Gemma
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable/disable debug mode

### Frontend Configuration
- Backend proxy is configured to `http://localhost:5000`
- CORS is enabled for local development
- File upload size limit: 16MB

## Edge Cases Handled

- **File Validation**: Checks file type and size before upload
- **Error Handling**: Comprehensive error handling for all operations
- **Database Integrity**: SQLite with proper error handling
- **File Overwriting**: Automatic file replacement with same name
- **API Failures**: Graceful handling of AI API failures
- **Empty States**: Proper handling of no jobs or no resume scenarios
- **Loading States**: User feedback during operations
- **Responsive Design**: Mobile-friendly interface

## Troubleshooting

### Common Issues

1. **Backend won't start:**
   - Check if virtual environment is activated
   - Verify all dependencies are installed
   - Check if port 5000 is available

2. **Frontend won't start:**
   - Ensure Node.js is installed
   - Check if port 3000 is available
   - Verify all npm packages are installed

3. **API connection errors:**
   - Ensure backend is running on port 5000
   - Check CORS configuration
   - Verify proxy settings in package.json

4. **File upload issues:**
   - Check file size (max 16MB)
   - Verify file format (PDF, DOCX, DOC)
   - Ensure backend resumeupload folder exists

5. **AI analysis fails:**
   - Verify Gemma API key is correct
   - Check internet connectivity
   - Ensure API endpoint is accessible

### Getting Help

- Check the console for error messages
- Verify all environment variables are set
- Ensure both backend and frontend are running
- Check network connectivity for AI API calls

## Development

### Backend Development
- Flask debug mode is enabled
- Database is automatically initialized
- CORS is enabled for frontend integration
- Comprehensive logging and error handling

### Frontend Development
- React development server with hot reload
- Modern ES6+ JavaScript
- Responsive CSS with modern design
- Component-based architecture

## Deployment

### Backend Deployment
- Use production WSGI server (Gunicorn, uWSGI)
- Set `FLASK_ENV=production`
- Configure proper database settings
- Set up environment variables securely

### Frontend Deployment
- Build production version: `npm run build`
- Serve static files from web server
- Configure backend API endpoint
- Set up proper CORS for production domain

## License

This project is open source and available under the MIT License.

## Improving Score Reliability

### Current AI Model
MatchLoop AI currently uses Google's Gemma 3 27B model for analysis. While this provides good results, here are ways to improve score reliability:

#### 1. **Enhanced Prompt Engineering**
- Refine the AI prompt to be more specific about evaluation criteria
- Add industry-specific terminology and requirements
- Include scoring rubrics and evaluation guidelines

#### 2. **Multiple AI Model Integration**
- Implement fallback to multiple AI providers (OpenAI GPT-4, Claude, etc.)
- Use ensemble methods to combine results from different models
- Implement model voting systems for more accurate scores

#### 3. **Training Data Enhancement**
- Collect feedback from HR professionals on analysis accuracy
- Build industry-specific training datasets
- Implement continuous learning from user corrections

#### 4. **Advanced Analysis Algorithms**
- Implement semantic similarity scoring using embeddings
- Add keyword density analysis with industry benchmarks
- Include experience level matching algorithms
- Implement skills gap analysis with learning path suggestions

#### 5. **Human-in-the-Loop Validation**
- Add manual review options for critical positions
- Implement confidence scoring for AI predictions
- Provide explanation for scoring decisions
- Allow HR professionals to adjust and validate scores

#### 6. **Industry-Specific Models**
- Train specialized models for different industries (tech, healthcare, finance)
- Implement domain-specific evaluation criteria
- Add industry-standard competency frameworks

#### 7. **Performance Metrics Tracking**
- Monitor accuracy rates over time
- Track false positive/negative rates
- Implement A/B testing for different analysis approaches
- Collect user satisfaction scores and feedback

### Implementation Priority
1. **Phase 1**: Enhanced prompt engineering and multiple AI model support
2. **Phase 2**: Industry-specific analysis and advanced algorithms
3. **Phase 3**: Machine learning from user feedback and continuous improvement
=======
# Matchloop-AI
MatchLoop AI is a full-stack web application that analyzes resume compatibility with job descriptions using LLM-based semantic analysis. Built with React and Python (Flask), it provides automated resume parsing, secure REST APIs, and dynamic match score generation with actionable skill-gap insights.
>>>>>>> 1ff10391eef4c9c6787adf146f8cb45494ddb7e2
