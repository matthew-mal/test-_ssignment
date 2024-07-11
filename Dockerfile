FROM python:3.12-alpine3.20

# Install dependencies for building Python packages and PostgreSQL client
RUN apk add postgresql-client build-base postgresql-dev

# Set working directory
WORKDIR /news_feed

# Copy requirements file and install dependencies
COPY requirements.txt /news_feed/requirements.txt
RUN pip install --no-cache-dir -r /news_feed/requirements.txt

# Copy the application code to the container
COPY . /news_feed

# Expose the port the application runs on
EXPOSE 8000

# Command to run the application
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
