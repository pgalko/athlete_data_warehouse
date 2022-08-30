FROM python:3.9

# set a directory for the app
WORKDIR /usr/src/athletedataapp

# copy all the files to the container
COPY . .

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install pg_dump
RUN apt-get update && apt-get -y install postgresql-client

# Install Chrome and chromedriver
# Install wget
RUN apt-get install -y wget
# Download and Install chrome
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# Download and Install chromedriver. The version here depends on what what version of chrome gets installed above !
RUN wget https://chromedriver.storage.googleapis.com/104.0.5112.79/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./web_app_loader_flask.py"]

#docker build -t pgalko/athlete_data_warehouse .

#docker run -it -e ENCR_PASS=0000 -v ./work_dir:/usr/src/athletedataapp/work_dir -p 5000:5000 pgalko/athlete_data_warehouse
#docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -v ./work_dir/db:/var/lib/postgresql/data -it postgres:13.5