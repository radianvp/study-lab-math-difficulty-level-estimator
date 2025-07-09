# 1. Base image (e.g., official Python)
FROM python:3.11-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Install system dependencies required for ffmpeg and other tools
RUN apt-get update && apt-get install -y \
    ffmpeg \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy the requirements file first (to leverage Docker cache)
COPY ./requirements.txt /app/

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the application files
COPY . /app


# 7. Expose the port used by Streamlit (default is 8501)
EXPOSE 8501

# 8. Command to run the Streamlit application
CMD ["streamlit", "run", "src/FAQStudy_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]