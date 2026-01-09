# Python Lab Environment
# Lightweight Python image for executing student code

FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Install common Python packages used in labs
RUN pip install --no-cache-dir \
    pytest \
    pylint \
    numpy \
    matplotlib

# Security: Run as non-root user
RUN useradd -m student
USER student

# Default command
CMD ["python", "main.py"]
