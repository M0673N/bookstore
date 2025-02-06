# Use a minimal base image
FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /bookstore

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies directly
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port for communication
EXPOSE 8000

# Install curl - necessary for healthcheck
RUN apk update && apk add --no-cache curl

# Create a non-root user for security
RUN adduser --disabled-password myuser
USER myuser

# Make database migrations and run the application
CMD ["sh", "-c", "python manage.py migrate && waitress-serve --port=8000 --threads=8 bookstore.wsgi:application"]