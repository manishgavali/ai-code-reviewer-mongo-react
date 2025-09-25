from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os, re, json

def run_checks(content: str):
    security = []
    if re.search(r'\beval\s*\(', content):
        security.append("Use of eval() detected — risky dynamic execution.")
    if re.search(r'\bexec\s*\(', content) or 'subprocess' in content or 'os.system' in content:
        security.append("Use of exec/subprocess/os.system — ensure inputs are sanitized.")
    if re.search(r"(SELECT|INSERT|UPDATE|DELETE).+\+", content, re.IGNORECASE):
        security.append("Possible SQL string concatenation — use parameterized queries.")
    if re.search(r"AKIA[A-Z0-9]{16}", content) or "-----BEGIN PRIVATE KEY-----" in content:
        security.append("Possible hard-coded secret or key detected.")
    if re.search(r"\\.innerHTML|dangerouslySetInnerHTML", content):
        security.append("Direct DOM insertion (innerHTML) — risk of XSS.")
    return security

def run_practices(content: str):
    practices = []
    if 'TODO' in content or 'FIXME' in content:
        practices.append('TODO/FIXME markers found — address before merge.')
    if len(content.splitlines()) > 500:
        practices.append('File is large (>500 lines) — consider splitting into modules.')
    if 'console.log(' in content:
        practices.append('console.log found — remove or guard debug logs.')
    if re.search(r'\bprint\s*\(', content) and '__name__' not in content:
        practices.append('print() call found — prefer logging in production code.')
    return practices

def find_duplicates(content: str):
    lines = [l.rstrip() for l in content.splitlines() if l.strip()!='']
    blocks = {}
    for i in range(len(lines)-3):
        block = '\n'.join(lines[i:i+4])
        blocks.setdefault(block, 0)
        blocks[block] += 1
    duplicates = [b for b,c in blocks.items() if c > 1]
    suggestions = []
    for d in duplicates[:5]:
        suggestions.append(f'Detected duplicated code block ({len(d)} chars) — consider extracting a function.')
    return suggestions

class FileItem(BaseModel):
    path: str
    content: str
    language: Optional[str] = 'auto'

class ReviewRequest(BaseModel):
    files: List[FileItem]
    repo: Optional[str] = None
    pr_number: Optional[int] = None


app = FastAPI(title='AI Code Reviewer (FastAPI+MongoDB Demo)')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/api/review')
def review(req: ReviewRequest):
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
    
    # Generate summary without OpenAI for now
        total_issues = sum(len(r['security']) + len(r['best_practices']) + len(r['refactor_suggestions']) for r in results)
        ai_summary = f"Code Review Summary:\nFound {total_issues} total issues."
        if total_issues > 0:
            if any(r['security'] for r in results):
                ai_summary += "\n- Security issues detected"
            if any(r['best_practices'] for r in results):
                ai_summary += "\n- Best practices improvements suggested"
            if any(r['refactor_suggestions'] for r in results):
                ai_summary += "\n- Code refactoring opportunities found"
    
    return {'review': {'results': results, 'ai_summary': ai_summary}}
