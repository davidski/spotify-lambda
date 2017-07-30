import os
import time
from datetime import date

import spotify_helpers as spot

if __name__ == "__main__":
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
    #print([e['track']['name'] for e in tracks])
