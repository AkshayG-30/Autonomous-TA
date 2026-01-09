"""
AI Tools
Tools that the AI agent can use to gather information about student code.
These enable the AI to "see" what's happening with the code.
"""

from typing import Optional
from app.grader.runner import run_code_in_sandbox


async def analyze_code_output(code: str, language: str = "python") -> dict:
    """
    Run the student's code and return the output.
    This lets the AI see what errors or output the code produces.
    """
    result = await run_code_in_sandbox(code, language)
    return {
        "success": result["success"],
        "output": result["output"][:1000],  # Limit output size
        "error": result.get("error", "")[:500],
        "timed_out": result.get("timed_out", False)
    }


def count_lines(code: str) -> int:
    """Count the number of lines in the code."""
    return len(code.strip().split('\n'))


def find_undefined_variables(code: str) -> list:
    """
    Simple static analysis to find potentially undefined variables.
    This is a basic implementation - in production, use proper AST analysis.
    """
    lines = code.split('\n')
    assigned = set()
    potentially_undefined = []
    
    for i, line in enumerate(lines, 1):
        # Very basic assignment detection
        if '=' in line and not line.strip().startswith('#'):
            parts = line.split('=')
            if len(parts) >= 2:
                var_part = parts[0].strip()
                # Handle simple assignments
                if var_part.isidentifier():
                    assigned.add(var_part)
    
    return list(potentially_undefined)


def check_for_infinite_loop_patterns(code: str) -> list:
    """
    Check for common infinite loop patterns.
    Returns a list of warnings.
    """
    warnings = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # while True without break
        if stripped.startswith('while True:'):
            # Check if there's a break in the subsequent lines
            has_break = any('break' in l for l in lines[i:i+10])
            if not has_break:
                warnings.append(f"Line {i}: `while True` loop - make sure there's a way to exit")
        
        # while <var> < x without incrementing
        if stripped.startswith('while '):
            # Very basic check - could be improved
            warnings.append(f"Line {i}: Found a while loop - verify the loop condition will eventually become False")
    
    return warnings
