# Dockerfile to create a container image  

# expand upon python base image 
FROM python:3.8-slim
# specify the working directory 
WORKDIR /app
# copy file from host to container image 
COPY . /app
COPY requirements.txt ./
# install app dependencies 
RUN pip install --no-cache-dir -r requirements.txt
# port image will expose
EXPOSE 5000
# default command for container to run 
CMD ["python", "app.py"]
