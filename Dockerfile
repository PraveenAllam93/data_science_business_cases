FROM python:3.11.0-slim-buster

WORKDIR /flask-churn-app


RUN python3 -m pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "-m","flask", "--app", "app.py", "run", "--host=0.0.0.0"]

# step 1: create the docker file, and define


# 1. Build the image by running the following command from the project root directory:
#     docker build -t <image_name> .
#           -t => tag name,
#           . => indicates Dockerfile is in current working directory
#  docker image ls -> gives list of images

# 2. Run the Docker container using the command shown below:
#     docker run -d -p 5000:5000 loan-prediction-pancakes # Here first 5000 is the port number of the host machine and second 5000 is the port number of the container.

# 3. To push a docker image named "ano" to docker hub, run the following command:
#     docker tag loan-prediction-pancakes:latest ano/loan-prediction-pancakes:latest
#     docker push ano/loan-prediction-pancakes:latest

