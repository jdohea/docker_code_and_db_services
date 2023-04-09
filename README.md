This application has a docker container with python code that takes gets the weather for 100 cities at at time of running and stores this data in a seperate dockerised mongo database.

Running "docker-compose up" should work perfectly.

This will fetch the python app from jdohea/python_weather_app:latest
Then also get the latest mongo image. The python app depends on this database image.

The python app will immediately run and input 100 records into the database. All the records in the database will the print, along with the sentence "NUMBER OF RECORDS AFTER RUN: XXX" where XXX is the number of records finally in the database.

This number will increment each time the python code is run. 

I tested running the python code, and that each run was adding more and more records into the database, by re-starting the pyton app image every time.

While i was testing the local python app, in the docker-compose.yml file instead of "image: jdohea/python_weather_app:latest" i had "build: ."

I then finally built the image, tagged it, and pushed it to my dockerhub repository and changed the compose file to pull from there.