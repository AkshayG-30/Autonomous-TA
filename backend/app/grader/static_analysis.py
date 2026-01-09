"""
Static Analysis
Linting and code quality checks for student submissions.
"""

import subprocess
import tempfile
import os
from typing import List, Dict


async def run_pylint(code: str) -> Dict:
    """
    Run pylint on Python code.
    Returns a dictionary with score and messages.
    """
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        result = subprocess.run(
            ["python", "-m", "pylint", temp_file, "--output-format=json", "--score=y"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Parse pylint output
        import json
        try:
            messages = json.loads(result.stdout) if result.stdout else []
        except json.JSONDecodeError:
            messages = []
        
        return {
            "success": result.returncode == 0,
            "score": extract_pylint_score(result.stderr),
            "messages": messages,
            "raw_output": result.stdout + result.stderr
        }
    
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Analysis timed out", "messages": []}
    
    except FileNotFoundError:
        return {"success": False, "error": "pylint not installed", "messages": []}
    
    finally:
        try:
            os.unlink(temp_file)
        except:
            pass


def extract_pylint_score(stderr: str) -> float:
    """Extract the pylint score from stderr output."""
    import re
    match = re.search(r'rated at ([\d.]+)/10', stderr)
    if match:
        return float(match.group(1))
    return 0.0


async def check_code_style(code: str, language: str = "python") -> List[Dict]:
    """
    Check code style issues.
    Returns a list of style suggestions.
    """
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Check line length
        if len(line) > 100:
            issues.append({
                "line": i,
                "type": "style",
                "message": "Line is too long (over 100 characters)"
            })
        
        # Check for trailing whitespace
        if line.rstrip() != line:
            issues.append({
                "line": i,
                "type": "style",
                "message": "Trailing whitespace"
            })
        
        # Check indentation (Python)
        if language == "python":
            stripped = line.lstrip()
            if stripped and line.startswith(' '):
                indent = len(line) - len(stripped)
                if indent % 4 != 0:
                    issues.append({
                        "line": i,
                        "type": "style",
                        "message": f"Inconsistent indentation (expected multiple of 4, got {indent})"
                    })
    
    return issues


async def analyze_code(code: str, language: str = "python") -> Dict:
    """
    Run all static analysis checks.
    """
    results = {
        "style_issues": await check_code_style(code, language),
        "line_count": len(code.split('\n')),
        "char_count": len(code)
    }
    
    if language == "python":
        pylint_result = await run_pylint(code)
        results["pylint"] = pylint_result
    
    return results
