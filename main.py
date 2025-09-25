from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import re

class FileItem(BaseModel):
    path: str
    content: str

class ReviewRequest(BaseModel):
    files: List[FileItem]

def run_checks(content: str):
    security = []
    if re.search(r'\beval\s*\(', content):
        security.append("Dangerous use of eval() detected")
    if re.search(r'\bexec\s*\(', content) or 'subprocess' in content or 'os.system' in content:
        security.append("Potentially dangerous system command execution detected")
    if re.search(r"(SELECT|INSERT|UPDATE|DELETE).+\+", content, re.IGNORECASE):
        security.append("Possible SQL injection vulnerability")
    return security

def run_practices(content: str):
    practices = []
    if 'print(' in content:
        practices.append("Consider using logging instead of print statements")
    if 'global ' in content:
        practices.append("Avoid using global variables")
    if 'except:' in content:
        practices.append("Avoid bare except clauses")
    return practices

def find_duplicates(content: str):
    # Simple duplicate line detection
    lines = content.split('\n')
    seen = set()
    duplicates = []
    for line in lines:
        if line.strip() and line in seen:
            duplicates.append(f"Duplicate line found: {line}")
        seen.add(line)
    return duplicates

app = FastAPI(title='AI Code Reviewer')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/review')
async def review(req: ReviewRequest):
    results = []
    for f in req.files:
        sec = run_checks(f.content)
        prac = run_practices(f.content)
        ref = find_duplicates(f.content)
        results.append({
            'path': f.path,
            'security': sec,
            'best_practices': prac,
            'refactor_suggestions': ref
        })
    
    return {
        "results": results,
        "ai_summary": "Code review completed successfully"
    }
