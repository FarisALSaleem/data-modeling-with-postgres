import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """Reads a JSON, extracted its artist, and song  records, and pushes them
    to the database.

    Parameters:
        cur (cursor): session cursor.
        filepath (string): Path to a JSON.
    """
    df = pd.read_json(filepath, lines=True)

    artist_data = df[["artist_id", "artist_name", "artist_location",
                      "artist_latitude", "artist_longitude"]].values[0]\
        .tolist()
    cur.execute(artist_table_insert, artist_data)

    song_data = df[["song_id", "title", "artist_id", "year", "duration"]]\
        .values[0].tolist()
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """Reads a JSON, extracted its time, user, and song play records, and
    pushes them to the database.

    Parameters:
        cur (cursor): session cursor.
        filepath (string): Path to a JSON.
    """
    df = pd.read_json(filepath, lines=True)

    df = df[df["page"] == "NextSong"]

    # convert timestamp column to datetime
    t = df.copy()
    t['ts'] = pd.to_datetime(df['ts'], unit='ms')

    time_data = (t["ts"].tolist(), t["ts"].dt.hour.tolist(),
                 t["ts"].dt.day.tolist(), t["ts"].dt.weekofyear.tolist(),
                 t["ts"].dt.month.tolist(), t["ts"].dt.year.tolist(),
                 t["ts"].dt.weekday.tolist())
    column_labels = ("timestamp", "hour", "day", "week of year", "month",
                     "year", "weekday")
    tson = {}
    for label, dlist in zip(column_labels, time_data):
        tson[label] = dlist

    time_df = pd.DataFrame(tson)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():

        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId,
                         row.level, songid, artistid, row.sessionId,
                         row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """finds all the JSON files in a path and commits a query function to them

    Parameters:
        cur (cursor): session cursor.
        conn (connection): database session.
        filepath (string): File path that contain JSONs.
        func (function): Query function to to apply to each JSON.
    """
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """Connects to sparkifydb extracts the data from the "data" folder and
     pushes it to the database.

    - Creates connects a sparkifydb and initiate a session.
    - Process data the data at data/song_data with the function
        process_song_file.
    - Process data the data at data/log_data with the function
        process_log_file.
    - The connection is terminated in the end.
    """
    conn = psycopg2.connect("""host=127.0.0.1 dbname=sparkifydb user=student
        password=student""")
    cur = conn.cursor()
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)
    cur.close()


if __name__ == "__main__":
    main()
