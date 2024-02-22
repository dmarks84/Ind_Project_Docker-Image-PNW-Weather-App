# Docker Image - Realtime PNW Weather Alert Website

## Screenshot
![WeatherApp](https://github.com/dmarks84/Ind_Project_Docker-Image-PNW-Weather-App/blob/main/WeatherApp_Screenshot.png?raw=true)

## Summary
I created a Docker Image that stands up a website which provides realtime weather alerts for the Pacific Northwest States (Oregon, Washington, Idaho, and Alaska).  The website was built in Python using Dash and API calls through the API services offered by the National Weather Service, a part of the National Oceanic and Atmospheric Administration (NOAA).  The data is cleaned and condensed, and a Folium map is built into an HTML IFrame image with markers color-coded by the alert severity.  Shapely polygons are illustrated and also color coded indicated the geographic range of the alert.  Red indicates Extreme alerts, orange Severe, and blue Moderate.  A dropdown menu allows the user to select their state of interest, and the header updates to know the date and time the information was called via the API using Requests.

The Docker Image is not currently shared via the Docker Hub.  However, a Dockerfile is included whihc allows the Image to be built.  All necessary files are included and simply need to be downloaded together to the directory of choice (no subfolders).  The Dockerfile exposes port 8050 within the Image, which is also the port that Dash is alerted to use.  Reference to localhost ports that might be indicated when the container is run shoudl be ignored; the local port can be selected by the user when running the Image as a container, as long as the mapped port is 8050.

A future iteration of this project will likely involve using a separate container for Apache Kafka, and using a Producer to publish the data into Kafka and a Consumer to digest it and save it to a database (or perhaps Kafka Connect can be utilized).

## Suggested Commands
**For building the image**

*Naming the Image weatherapp*

docker build --tag weatherapp .

**For starting a container on local port localhost:9092:**

*Naming the container weatherapp_cont*

docker run -it --name weatherapp_cont -p 9092:8050 weatherapp:latest

## Skills (Developed & Applied)
Programming, Python, Docker, Dockerfile, Images, Devops, Folium, Dash, Plotly, Requests, API, GeoPandas, JSON, web applications, websites
