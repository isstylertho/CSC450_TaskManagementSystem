# Use a Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /app

# Expose the port the app will run on
EXPOSE 5000

# Set the environment variable to disable buffering of the output (helps with logging)
ENV PYTHONUNBUFFERED=1

# Command to run the app
CMD ["flask", "run", "--host=0.0.0.0"]
