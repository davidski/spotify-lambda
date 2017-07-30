Spotify-History
================

Python based AWS Lambda function for building an offline list of played 
tracks from Spotify.

When triggered, this function polls the Spotify API for all tracks played 
on the current date. As the Spotify API returns no more than 50 tracks, 
this function is intended to be ran several times a day. It first looks for an 
existing day's history file in S3. Any found history file is merged with the 
results from the API, using the `played_at` key to deduplicate.

Expected Environment Variables
------------------------------

+ SPOTIFY_BUCKET_NAME - Name of S3 bucket to store data and token files.
+ SPOTIFY_BUCKET_KEY - Optional key under which to store data and token files.
+ SPOTIFY_CLIENT_ID - Application OAuth client ID.
+ SPOTIFY_CLIENT_NAME - Application OAuth client secret.

Deployment
----------

The included [Makefile](./Makefile) will build a ZIP file which can be 
deployed to AWS Lambda. This ZIP file will include all dependencies. 

Contributing
============

This project is governed by a [Code of Conduct](./CODE_OF_CONDUCT.md). By 
participating in this project you agree to abide by these terms.

License
=======

The [MIT License](LICENSE) applies.
