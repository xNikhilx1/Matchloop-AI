import os
import sqlite3
import json
import re
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import PyPDF2
from docx import Document
import requests
from dotenv import load_dotenv
import uuid
import google.generativeai as genai

# from google import genai
# Load environment variables
load_dotenv('config.env')

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'resumeupload'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


# Database initialization
def init_db():
    conn = sqlite3.connect('resume_parser.db')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS job_positions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       position_name
                       TEXT
                       NOT
                       NULL,
                       job_description
                       TEXT
                       NOT
                       NULL,
                       created_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   ''')
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def perform_basic_analysis(resume_text, job_description):
    """Perform basic keyword-based analysis when AI fails"""
    try:
        # Convert to lowercase for comparison
        resume_lower = resume_text.lower()
        job_lower = job_description.lower()

        # Common skills and keywords
        technical_skills = ['python', 'javascript', 'java', 'react', 'angular', 'node.js', 'sql', 'mongodb', 'aws',
                            'docker', 'kubernetes', 'git', 'html', 'css', 'typescript', 'php', 'c++', 'c#', '.net',
                            'spring', 'django', 'flask', 'express', 'vue', 'jquery', 'bootstrap', 'sass', 'less',
                            'webpack', 'babel', 'npm', 'yarn']

        soft_skills = ['leadership', 'communication', 'teamwork', 'problem solving', 'project management', 'agile',
                       'scrum', 'collaboration', 'time management', 'adaptability', 'creativity', 'critical thinking',
                       'decision making', 'mentoring', 'training', 'presentation', 'negotiation', 'customer service']

        # Count matching skills
        technical_matches = sum(1 for skill in technical_skills if skill in resume_lower and skill in job_lower)
        soft_matches = sum(1 for skill in soft_skills if skill in resume_lower and skill in job_lower)

        # Calculate basic score (0-100)
        total_skills = len([skill for skill in technical_skills + soft_skills if skill in job_lower])
        if total_skills > 0:
            score = min(100, int((technical_matches + soft_matches) / total_skills * 100))
        else:
            score = 50  # Default score if no skills found

        # Generate basic analysis
        strengths = []
        if technical_matches > 0:
            strengths.append(f"Matches {technical_matches} technical skills required")
        if soft_matches > 0:
            strengths.append(f"Matches {soft_matches} soft skills required")
        if not strengths:
            strengths.append("Basic keyword analysis completed")

        weaknesses = []
        if score < 70:
            weaknesses.append("Consider adding more relevant skills to your resume")
            weaknesses.append("Highlight specific project experiences")

        analysis = f"Basic analysis completed. Found {technical_matches} technical skill matches and {soft_matches} soft skill matches. This is a fallback analysis due to AI service unavailability."

        return {
            'compatibility_score': score,
            'strengths': strengths,
            'weaknesses': weaknesses,
            'analysis': analysis
        }

    except Exception as e:
        return {
            'compatibility_score': 50,
            'strengths': ['Basic analysis available'],
            'weaknesses': ['AI analysis unavailable'],
            'analysis': f'Fallback analysis completed. AI service error: {str(e)}'
        }


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return ""


def analyze_resume_with_ai(resume_text, job_description):
    """Analyze resume compatibility with job description using Google's Gemma AI"""
    try:
        api_key = os.getenv('GEMMA_API_KEY')

        if not api_key:
            return {
                'compatibility_score': 0,
                'strengths': ['API key not configured'],
                'weaknesses': ['Please configure your Gemma API key'],
                'analysis': 'Unable to analyze resume due to missing API configuration'
            }

        # Configure Google Generative AI
        genai.configure(api_key=api_key)

        # Prepare prompt for AI analysis
        prompt = f"""
        Analyze the compatibility between this resume and job description.

        Job Description:
        {job_description}

        Resume:
        {resume_text}

        Please provide:
        1. A compatibility score (0-100)
        2. List of strengths that match the job requirements
        3. List of weaknesses or areas for improvement
        4. Overall analysis and recommendations

        Format your response as JSON with keys: compatibility_score, strengths, weaknesses, analysis
        """

        try:
            # Use Google's official client
            model = genai.GenerativeModel('gemma-3-27b-it')
            response = model.generate_content(prompt)

            if response.text:
                ai_response = response.text

                # Try to parse JSON response - handle markdown-wrapped JSON
                try:
                    # Clean the response - remove markdown code blocks if present
                    cleaned_response = ai_response.strip()
                    if cleaned_response.startswith('```json'):
                        cleaned_response = cleaned_response[7:]  # Remove ```json
                    if cleaned_response.startswith('```'):
                        cleaned_response = cleaned_response[3:]  # Remove ```
                    if cleaned_response.endswith('```'):
                        cleaned_response = cleaned_response[:-3]  # Remove ```

                    cleaned_response = cleaned_response.strip()
                    parsed_response = json.loads(cleaned_response)
                    return parsed_response
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
                    print(f"AI response: {ai_response}")
                    # If AI response is not valid JSON, create a structured response
                    return {
                        'compatibility_score': 75,
                        'strengths': ['AI analysis completed'],
                        'weaknesses': ['Response format parsing issue'],
                        'analysis': ai_response
                    }
            else:
                return {
                    'compatibility_score': 0,
                    'strengths': [],
                    'weaknesses': ['Empty AI response'],
                    'analysis': 'AI returned empty response'
                }

        except Exception as api_error:
            print(f"Google AI API error: {api_error}")
            return {
                'compatibility_score': 0,
                'strengths': [],
                'weaknesses': ['Google AI API error'],
                'analysis': f'Google AI API error: {str(api_error)}'
            }

    except Exception as e:
        return {
            'compatibility_score': 0,
            'strengths': [],
            'weaknesses': [f'Error: {str(e)}'],
            'analysis': f'Error occurred during AI analysis: {str(e)}'
        }


@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """Get all job positions"""
    try:
        conn = sqlite3.connect('resume_parser.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM job_positions ORDER BY created_at DESC')
        jobs = cursor.fetchall()

        job_list = []
        for job in jobs:
            job_list.append({
                'id': job[0],
                'position_name': job[1],
                'job_description': job[2],
                'created_at': job[3]
            })

        conn.close()
        return jsonify({'jobs': job_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs', methods=['POST'])
def create_job():
    """Create a new job position"""
    try:
        data = request.get_json()
        position_name = data.get('position_name')
        job_description = data.get('job_description')

        if not position_name or not job_description:
            return jsonify({'error': 'Position name and job description are required'}), 400

        conn = sqlite3.connect('resume_parser.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO job_positions (position_name, job_description) VALUES (?, ?)',
            (position_name, job_description)
        )
        conn.commit()
        job_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'message': 'Job created successfully',
            'job_id': job_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get a specific job position"""
    try:
        conn = sqlite3.connect('resume_parser.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM job_positions WHERE id = ?', (job_id,))
        job = cursor.fetchone()
        conn.close()

        if job:
            return jsonify({
                'id': job[0],
                'position_name': job[1],
                'job_description': job[2],
                'created_at': job[3]
            })
        else:
            return jsonify({'error': 'Job not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and process resume file"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['resume']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF and DOCX files are allowed'}), 400

        # Save file as resume_1 with original extension
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f'resume_1.{file_extension}'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        file.save(file_path)

        return jsonify({
            'message': 'Resume uploaded successfully',
            'filename': filename,
            'file_path': file_path
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze-resume', methods=['POST'])
def analyze_resume():
    """Analyze resume compatibility with selected job"""
    try:
        data = request.get_json()
        job_id = data.get('job_id')

        if not job_id:
            return jsonify({'error': 'Job ID is required'}), 400

        # Get job details
        conn = sqlite3.connect('resume_parser.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM job_positions WHERE id = ?', (job_id,))
        job = cursor.fetchone()
        conn.close()

        if not job:
            return jsonify({'error': 'Job not found'}), 404

        job_description = job[2]

        # Check if resume exists
        resume_path = None
        for ext in ['pdf', 'docx', 'doc']:
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'resume_1.{ext}')
            if os.path.exists(temp_path):
                resume_path = temp_path
                break

        if not resume_path:
            return jsonify({'error': 'No resume found. Please upload a resume first.'}), 400

        # Extract text from resume
        if resume_path.endswith('.pdf'):
            resume_text = extract_text_from_pdf(resume_path)
        elif resume_path.endswith(('.docx', '.doc')):
            resume_text = extract_text_from_docx(resume_path)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        if not resume_text.strip():
            return jsonify({'error': 'Could not extract text from resume'}), 400

        # Analyze with AI
        analysis_result = analyze_resume_with_ai(resume_text, job_description)

        # If AI analysis fails, provide a basic fallback analysis
        if analysis_result.get('compatibility_score') == 0 and 'Error' in str(analysis_result.get('analysis', '')):
            # Basic keyword-based fallback analysis
            analysis_result = perform_basic_analysis(resume_text, job_description)

        return jsonify({
            'job_position': job[1],
            'resume_filename': os.path.basename(resume_path),
            'resume_text': resume_text[:500] + '...' if len(resume_text) > 500 else resume_text,
            'resume_full_text': resume_text,  # Full text for detailed analysis
            'analysis': analysis_result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Resume Parser AI Backend is running'})


if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
    print("Starting Flask application...")
    app.run(debug=True, host='0.0.0.0', port=5000)
