FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose ports for Flask and Streamlit (if both are to be run)
EXPOSE 5000 8501

# Command to run the Flask app
CMD ["python", "app_flask.py"]
