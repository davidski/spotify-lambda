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
+ SPOTIFY_BUCKET_KEY - Optional key under which to store data and token files. Must not have a leading slash.
+ SPOTIFY_CLIENT_ID - Application OAuth client ID.
+ SPOTIFY_CLIENT_NAME - Application OAuth client secret.

Deployment
----------

The included [Makefile](./Makefile) will build a ZIP file which can be 
deployed to AWS Lambda. This ZIP file will include all dependencies.

The Spotify API uses OAuth authentication. The initial setup of tokens 
requires user interaction to authorize this application. To carry out first 
time setup, run the `authorize.py` script in an interactive window. This will 
prompt the user to visit a Spotify URL and authorize the application. Upon 
authorization, the user's browser will be redirected to a non-resolving URL. 
Copy that full URL and paste into the python console. The `authorize.py` script 
will take that response URL, obtain a OAuth token from Spotify, and save it in a 
`token.json` file in the S3 bucket configured in the environment variables. Future 
runs of the `main.py` process do not require authorization as long as the function 
can auto-renew the token. If this function is run at least every 12 hours, that 
should not be a problem (renew token lengths are approximately 15 hours).

Contributing
============

This project is governed by a [Code of Conduct](./CODE_OF_CONDUCT.md). By 
participating in this project you agree to abide by these terms.

License
=======

The [MIT License](LICENSE) applies.
