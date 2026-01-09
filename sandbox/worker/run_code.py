"""
Sandbox Worker Script
Utility script that runs inside the Docker container.
Handles code execution, output capture, and timeout management.
"""

import sys
import time
import traceback


def run_student_code(code_path: str) -> dict:
    """
    Execute the student's code file and capture output.
    
    Args:
        code_path: Path to the Python file to execute
    
    Returns:
        dict with success, output, error
    """
    import io
    from contextlib import redirect_stdout, redirect_stderr
    
    stdout_capture = io.StringIO()
    stderr_capture = io.StringIO()
    
    start_time = time.time()
    
    try:
        with open(code_path, 'r') as f:
            code = f.read()
        
        with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
            exec(compile(code, code_path, 'exec'), {'__name__': '__main__'})
        
        execution_time = time.time() - start_time
        
        return {
            'success': True,
            'output': stdout_capture.getvalue(),
            'error': stderr_capture.getvalue(),
            'execution_time': execution_time
        }
    
    except Exception as e:
        execution_time = time.time() - start_time
        
        return {
            'success': False,
            'output': stdout_capture.getvalue(),
            'error': traceback.format_exc(),
            'execution_time': execution_time
        }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python run_code.py <code_file>")
        sys.exit(1)
    
    result = run_student_code(sys.argv[1])
    
    # Print output
    if result['output']:
        print(result['output'], end='')
    
    # Print errors to stderr
    if result['error']:
        print(result['error'], file=sys.stderr, end='')
    
    sys.exit(0 if result['success'] else 1)
