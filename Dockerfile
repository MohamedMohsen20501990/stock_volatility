# start the python base image
FROM python:3.10

# set the working directory inside the container
WORKDIR /app

# add requirement file to the image
COPY ./requirements.txt /app/requirements.txt

# install all required packages and libraries
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# add python codes
COPY . .

# specify default commands to start the fastapi app
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "80"]




