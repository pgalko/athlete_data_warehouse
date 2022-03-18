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

# define the port number the container should expose
EXPOSE 5000

# run the command
CMD ["python", "./web_app_loader_flask.py"]

#docker build -t pgalko/athlete_data_warehouse .

#docker run -it -e ENCR_PASS=0000 -v ./work_dir:/usr/src/athletedataapp/work_dir -p 5000:5000 pgalko/athlete_data_warehouse
#docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -v ./work_dir/db:/var/lib/postgresql/data -it postgres:13.5