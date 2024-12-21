# Use Python 3.12 for compatibility
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file to the container
COPY requirements.txt .

# Install required Python packages
RUN pip3 install --upgrade pip \
    && pip3 install -U -r Requirments.txt

# Copy the rest of the application files to the container
COPY . .

# Expose a port for platforms requiring it (e.g., Heroku, Koyeb, Render)
EXPOSE 8080

# Command to run the bot using main.py
CMD ["python3", "main.py"]
