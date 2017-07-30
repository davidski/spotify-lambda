import os
import time
from datetime import date

from functions import spotify_helpers as spot

# Spotify application Oauth credentials
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Spotify token and history URIs
endpoint_uri = 'https://api.spotify.com/v1/me/player/recently-played'
token_uri = 'https://accounts.spotify.com/api/token'

# bucket and path to store daily files
bucket = os.getenv("SPOTIFY_BUCKET_NAME")
path = os.getenv("SPOTIFY_BUCKET_PATH")

if __name__ == "main":
    current_date = date.isoformat(date.today())
    current_timestamp = int(time.mktime(date.today().timetuple()))

    # read in existing file
    tracks = spot.read_s3_file(current_date)

    # get new tracks, starting from today at midnight
    new_tracks = spot.fetch_all_tracks(after=current_timestamp)

    # merge and deduplicate tracks
    tracks.extend(new_tracks)
    tracks = {i['played_at']: i for i in tracks}.values()

    # write out file
    spot.write_s3_file(tracks, current_date)
    print([e['track']['name'] for e in tracks])
