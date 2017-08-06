from requests_oauthlib import OAuth2Session
import boto3
import botocore
import json
import os
import logging

# set up logging
logger = logging.getLogger('PySpotify')


def fetch_token():
    """ reads the client oauth token from S3 """
    bucket = os.environ["SPOTIFY_BUCKET_NAME"]
    path = os.getenv("SPOTIFY_BUCKET_PATH", "")
    logger.info("Reading Spotify OAuth token from s3://%s/%s/token.json." %
                (bucket, path))
    s3 = boto3.client('s3')
    content_object = s3.get_object(Bucket=bucket, Key="%s/token.json" % path)
    file_content = content_object['Body'].read().decode('utf-8')
    token = json.loads(file_content)
    return token


def save_token(token):
    """ saves a client oauth token to S3 """
    logger.info("Saving token to S3.")
    bucket = os.environ["SPOTIFY_BUCKET_NAME"]
    path = os.getenv("SPOTIFY_BUCKET_PATH", "")
    s3 = boto3.client('s3')
    data = json.dumps(token)
    s3.put_object(Bucket=bucket, Key="%s/token.json" % path, Body=data)
    return


def fetch_uri(uri):
    """ fetch a oauth protected url """
    logger.info("Working on uri: %s" % uri)
    token = fetch_token()
    token_uri = 'https://accounts.spotify.com/api/token'
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    extra = {'client_id': client_id, 'client_secret': client_secret}

    client = OAuth2Session(client_id, token=token,
                           auto_refresh_url=token_uri,
                           auto_refresh_kwargs=extra,
                           token_updater=save_token)
    r = client.get(uri)

    return r.json()


def fetch_all_tracks(after):
    """ retrieve full history from Spotify """
    endpoint_uri = 'https://api.spotify.com/v1/me/player/recently-played'
    tracks = []
    data = fetch_uri(endpoint_uri + "?after=%s" % after)
    tracks.extend(data['items'])
    while 'next' in data:
        data = fetch_uri(data['next'])
        tracks.extend(data['items'])
    logger.info("Returning %s tracks." % len(tracks))
    return tracks


def read_s3_file(date):
    """ retrieve an optionally present file of the day's play """
    """ history from S3 """
    bucket = os.getenv("SPOTIFY_BUCKET_NAME")
    path = os.getenv("SPOTIFY_BUCKET_PATH")
    s3 = boto3.resource('s3')
    try:
        s3.Object(bucket, "%s/%s.json" % (path, date)).load()
    except botocore.exceptions.ClientError as e:
        logger.info("No existing history file found for %s, %s" %
                    (date, e.response['Error']['Code']))
        if e.response['Error']['Code'] == '404':
            return []
        else:
            logger.warning("Unexpected error code returned!")
            return []
    else:
        logger.info("Reading history file for %s" % date)
        content_object = s3.Object(bucket, "%s/%s.json" % (path, date))
        file_content = content_object.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        return json_content


def write_s3_file(data, date):
    """ save the day's history file to S3 """
    logger.info("Writing history file to S3.")
    bucket = os.getenv("SPOTIFY_BUCKET_NAME")
    path = os.getenv("SPOTIFY_BUCKET_PATH")
    s3 = boto3.client('s3')
    data = json.dumps(data)
    s3.put_object(Bucket=bucket, Key="%s/%s.json" % (path, date), Body=data)
