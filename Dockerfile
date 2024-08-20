# Pulls base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

# Set work directory 
WORKDIR /code

COPY requirements.txt /code/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements1.txt

# Copy project
COPY . /code/

# CMD ["python", "manage.py", "makemigrations", "--noinput"]
# CMD ["python", "manage.py", "migrate", "--noinput"]
# CMD ["python", " manage.py", " collectstatic"]

# ENTRYPOINT ["./docker-entrypoint.sh"]