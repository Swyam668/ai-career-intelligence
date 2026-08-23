# official python image - slim is lite version
FROM python:3.11-slim

# working directory in container
WORKDIR /app

# System dependencies for PDF parsing and ML libraries
# update package lists
RUN apt-get update && apt-get install -y \
# for compilers/build tools needed by some Python ML libraries
    build-essential \
    # tools for PDF processing.
    poppler-utils \
    # to remove cached package lists so that docker image is small
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# preveting storafe of cached files -- image size small
RUN pip install --no-cache-dir -r requirements.txt

#copy . (local directory) files into container (second dot . is for /app working directory in container) 
COPY . .

#port
EXPOSE 7860

# running command
# 0.0.0.0 -> allow access from outside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]