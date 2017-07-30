#!/bin/env python

import time
import datetime
import logging
import spotify_helpers as spot

# set up logging
logger = logging.getLogger('PySpotify')
logger.setLevel(logging.INFO)
if not len(logger.handlers):
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - ' +
                                  '%(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def update_played_track_history(desired_date):
    """ update a day's current played history """
    logger.info("Retrieving played song history for %s" % desired_date)
    full_datetime = datetime.datetime.combine(desired_date, datetime.time())
    starting_timestamp = int(time.mktime(full_datetime.timetuple()) * 1000)

    # read in existing file
    tracks = spot.read_s3_file(datetime.date.isoformat(desired_date))

    # get new tracks, starting from today at midnight
    new_tracks = spot.fetch_all_tracks(after=starting_timestamp)

    # merge and deduplicate tracks
    tracks.extend(new_tracks)
    tracks = list({i['played_at']: i for i in tracks}.values())

    # write out file
    spot.write_s3_file(tracks, datetime.date.isoformat(desired_date))
    # print([e['track']['name'] for e in tracks])


def lambda_handler(event=None, context=None):
    """ main Lambda event handling loop """
    update_played_track_history(datetime.date.today())


if __name__ == "__main__":
    update_played_track_history(datetime.date.today() - datetime.timedelta(0))
