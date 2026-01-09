"""
Sandbox Code Runner
Securely executes student code in isolated Docker containers.
Provides timeout protection and resource limits.
"""

import asyncio
import tempfile
import os
from pathlib import Path
from typing import Optional

# Docker is optional - fallback to subprocess if not available
try:
    import docker
    from docker.errors import ContainerError, ImageNotFound, APIError
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False
    docker = None

from app.core.config import settings


# Docker client
client = None


def get_docker_client():
    """Get or create Docker client."""
    global client
    if not DOCKER_AVAILABLE:
        return None
    if client is None:
        try:
            client = docker.from_env()
        except Exception as e:
            print(f"⚠️ Docker not available: {e}")
            return None
    return client


# Image mapping for different languages
LANGUAGE_IMAGES = {
    "python": "python:3.11-slim",
    "python3": "python:3.11-slim",
    "cpp": "gcc:latest",
    "c": "gcc:latest",
    "java": "openjdk:17-slim"
}

# Run commands for different languages
RUN_COMMANDS = {
    "python": "python /code/main.py",
    "python3": "python /code/main.py",
    "cpp": "g++ /code/main.cpp -o /code/main && /code/main",
    "c": "gcc /code/main.c -o /code/main && /code/main",
    "java": "cd /code && javac Main.java && java Main"
}

# File extensions for different languages
FILE_EXTENSIONS = {
    "python": "py",
    "python3": "py",
    "cpp": "cpp",
    "c": "c",
    "java": "java"
}


async def run_code_in_sandbox(
    code: str,
    language: str = "python",
    timeout: Optional[int] = None
) -> dict:
    """
    Execute code in an isolated Docker container.
    
    Args:
        code: The code to execute
        language: Programming language (python, cpp, c, java)
        timeout: Execution timeout in seconds (default from settings)
    
    Returns:
        dict with success, output, error, execution_time, timed_out
    """
    docker_client = get_docker_client()
    
    # Fallback to subprocess if Docker is not available
    if docker_client is None:
        return await run_code_fallback(code, language, timeout)
    
    timeout = timeout or settings.sandbox_timeout
    language = language.lower()
    
    # Get configuration for the language
    image = LANGUAGE_IMAGES.get(language, "python:3.11-slim")
    run_cmd = RUN_COMMANDS.get(language, "python /code/main.py")
    file_ext = FILE_EXTENSIONS.get(language, "py")
    
    # Create temporary directory with the code
    with tempfile.TemporaryDirectory() as tmpdir:
        # Write code to file
        filename = "Main.java" if language == "java" else f"main.{file_ext}"
        code_file = Path(tmpdir) / filename
        code_file.write_text(code, encoding="utf-8")
        
        try:
            # Run container
            container = docker_client.containers.run(
                image=image,
                command=f"sh -c '{run_cmd}'",
                volumes={tmpdir: {"bind": "/code", "mode": "rw"}},
                mem_limit=settings.sandbox_memory_limit,
                network_disabled=True,  # No network access
                remove=True,
                detach=True
            )
            
            # Wait for completion with timeout
            try:
                result = container.wait(timeout=timeout)
                logs = container.logs().decode("utf-8")
                
                return {
                    "success": result["StatusCode"] == 0,
                    "output": logs,
                    "error": "" if result["StatusCode"] == 0 else logs,
                    "execution_time": None,
                    "timed_out": False
                }
            
            except Exception as timeout_error:
                # Timeout - kill the container
                try:
                    container.kill()
                    container.remove()
                except:
                    pass
                
                return {
                    "success": False,
                    "output": "",
                    "error": "⏰ Execution timed out. Your code may have an infinite loop.",
                    "execution_time": timeout,
                    "timed_out": True
                }
        
        except ContainerError as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "execution_time": None,
                "timed_out": False
            }
        
        except ImageNotFound:
            return {
                "success": False,
                "output": "",
                "error": f"Docker image not found: {image}. Run `docker pull {image}` first.",
                "execution_time": None,
                "timed_out": False
            }
        
        except APIError as e:
            return {
                "success": False,
                "output": "",
                "error": f"Docker API error: {e}",
                "execution_time": None,
                "timed_out": False
            }


async def run_code_fallback(
    code: str,
    language: str = "python",
    timeout: Optional[int] = None
) -> dict:
    """
    Fallback execution using subprocess when Docker is not available.
    ⚠️ Less secure - only use in development!
    """
    import subprocess
    import time
    
    timeout = timeout or settings.sandbox_timeout
    
    if language not in ["python", "python3"]:
        return {
            "success": False,
            "output": "",
            "error": f"Fallback mode only supports Python. Docker required for {language}.",
            "execution_time": None,
            "timed_out": False
        }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write(code)
        temp_file = f.name
    
    try:
        start_time = time.time()
        
        result = subprocess.run(
            ["python", temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        execution_time = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "execution_time": execution_time,
            "timed_out": False
        }
    
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "⏰ Execution timed out. Your code may have an infinite loop.",
            "execution_time": timeout,
            "timed_out": True
        }
    
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": str(e),
            "execution_time": None,
            "timed_out": False
        }
    
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except:
            pass
