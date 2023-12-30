# Use an official Python runtime as the base image
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /code
# Install dependencies
COPY requirements.txt /code/
RUN pip install -r requirements.txt
RUN pip install mysqlclient
# Copy the Django project code into the container
COPY . /code/

# Expose the port that Django runs on
EXPOSE 8001

RUN python manage.py migrate
RUN python manage.py collectstatic

# Start the Django development server
CMD ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi:application"]