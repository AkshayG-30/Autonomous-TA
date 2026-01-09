# C++ Lab Environment
# GCC compiler for C/C++ student code

FROM gcc:latest

# Set working directory
WORKDIR /code

# Install additional tools
RUN apt-get update && apt-get install -y \
    make \
    valgrind \
    && rm -rf /var/lib/apt/lists/*

# Security: Run as non-root user
RUN useradd -m student
USER student

# Default command (compile and run)
CMD ["sh", "-c", "g++ -o main main.cpp && ./main"]
