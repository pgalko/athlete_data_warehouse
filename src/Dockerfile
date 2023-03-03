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
# New 20230303: Pulls and installs an older version of chrome. The latest version of chrome is not compatible with the latest version of chromedriver
RUN wget http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_108.0.5359.71-1_amd64.deb
RUN apt-get install -y ./google-chrome-stable_108.0.5359.71-1_amd64.deb
# Original before 20230303:
#RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb
# Check chrome version
RUN echo "Chrome: " && google-chrome --version
# Download and Install chromedriver. The version here depends on what what version of chrome gets installed above !
# The lastest chrome versions can be checked here: https://www.ubuntuupdates.org/package/google_chrome/stable/main/base/google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

# define the port number the container should expose
EXPOSE 5000

#docker build -t pgalko/athlete_data_warehouse .
