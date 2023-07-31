FROM python:3.11
#This command will create the working directory for our Python Flask application Docker image
WORKDIR /app
#This command will copy the dependencies and libraries in the requirements.txt to the working directory
COPY requirements.txt /app
#This command will install the dependencies in the requirements.txt to the Docker image
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
#This command will copy the files and source code required to run the application
COPY . /app
#This command will start the Python Flask application Docker container
CMD python wsgi.py


