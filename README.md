# Youtube Hit Analyzer

Youtube Hit Analyzer is a tool to that helps us determine whether a combination of 
**title** and **thumbnail** for a video will produce a **hit video** _( a hit video has a much higher click through rate resulting in significantly more views)_.

## What is a hit video ? 
A hit video is a video what has **3 times** more views when compared with the **simple average** of the last 3 videos for a given youtube channel, for example:

![hit video](https://i.ibb.co/c1XS5SV/hit-video.png "Logo Title Text 1")

## What is in the youtube analyzer
The youtube hit analyzer is a set of micro-apps working together to understand what makes a hit video, the system contains:

+ Integration with google sheets to save data
+ Integration with [youtube api](https://developers.google.com/youtube/v3) to ease the scrapping process
+ A video scrapper of raw data
+ Dataset creation with the video data
+ Labeling of hit videos
+ A Classifier of new videos with neural nets


## How to use
You can run the application inside a Docker container to simplify the installation requirements. To run **with docker** you need:

+ Install [docker in your machine](https://docs.docker.com/get-docker/) 
+ [Create a youtube api key](https://developers.google.com/youtube/v3/getting-started)
+ [Enable access to google sheets api](https://developers.google.com/sheets/api/quickstart/python)
+ Clone the project repository in your machine
+ Go to the root folder in the youtube-analyzer project and copy the `credentials.json` containing information about your [**google sheets api**](https://developers.google.com/sheets/api/guides/authorizing).
+ Run the commands: `docker build -t yt-analyzer` and `docker run yt-analyzer -e 'YOUTUBE-API-KEY'`