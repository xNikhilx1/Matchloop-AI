#!/usr/bin/env python3
"""
Simple test script to verify the backend is working correctly.
Run this after starting the backend to test basic functionality.
"""

import requests
import json
import time

def test_backend():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Resume Parser AI Backend")
    print("=" * 50)
    
    # Test 1: Health Check
    print("\n1. Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on port 5000")
        return False
    
    # Test 2: Get Jobs (should be empty initially)
    print("\n2. Testing Get Jobs...")
    try:
        response = requests.get(f"{base_url}/api/jobs")
        if response.status_code == 200:
            jobs = response.json()['jobs']
            print(f"✅ Get jobs passed: {len(jobs)} jobs found")
        else:
            print(f"❌ Get jobs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get jobs error: {e}")
        return False
    
    # Test 3: Create Job
    print("\n3. Testing Create Job...")
    test_job = {
        "position_name": "Test Software Engineer",
        "job_description": "This is a test job description for testing purposes. Skills required: Python, JavaScript, React."
    }
    
    try:
        response = requests.post(f"{base_url}/api/jobs", json=test_job)
        if response.status_code == 201:
            job_id = response.json()['job_id']
            print(f"✅ Create job passed: Job ID {job_id}")
        else:
            print(f"❌ Create job failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Create job error: {e}")
        return False
    
    # Test 4: Get Jobs Again (should have 1 job now)
    print("\n4. Testing Get Jobs After Creation...")
    try:
        response = requests.get(f"{base_url}/api/jobs")
        if response.status_code == 200:
            jobs = response.json()['jobs']
            print(f"✅ Get jobs after creation: {len(jobs)} jobs found")
            if len(jobs) > 0:
                print(f"   Latest job: {jobs[0]['position_name']}")
        else:
            print(f"❌ Get jobs after creation failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get jobs after creation error: {e}")
        return False
    
    # Test 5: Get Specific Job
    print("\n5. Testing Get Specific Job...")
    try:
        response = requests.get(f"{base_url}/api/jobs/{job_id}")
        if response.status_code == 200:
            job = response.json()
            print(f"✅ Get specific job passed: {job['position_name']}")
        else:
            print(f"❌ Get specific job failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Get specific job error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All basic tests passed! Backend is working correctly.")
    print("\nNext steps:")
    print("1. Configure your Gemma AI API key in backend/config.env")
    print("2. Start the frontend with 'npm start' in the frontend directory")
    print("3. Open http://localhost:3000 in your browser")
    print("4. Test the full application workflow")
    
    return True

if __name__ == "__main__":
    print("Make sure the backend is running before executing this test!")
    print("To start the backend:")
    print("1. cd backend")
    print("2. .venv\\Scripts\\activate (Windows) or source .venv/bin/activate (Linux/Mac)")
    print("3. python app.py")
    print()
    
    input("Press Enter to continue with the test...")
    
    if test_backend():
        print("\n✅ Backend test completed successfully!")
    else:
        print("\n❌ Backend test failed. Check the errors above.")
    
    input("\nPress Enter to exit...")
