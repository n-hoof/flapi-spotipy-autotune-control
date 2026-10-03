import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
redirect_uri=os.getenv("REDIRECT_URI")

RECCO_BEATS_BASE_URL='https://api.reccobeats.com/v1/audio-features?ids='
RECCO_BEATS_KEY_MAP={
    0: "C",
    1: "Db",
    2: "D",
    3: "Eb",
    4: "E",
    5: "F",
    6: "Gb",
    7: "G",
    8: "Ab",
    9: "A",
    10: "Bb",
    11: "B",
    12: "C",
    13: "Db",
    14: "D",
}

def create_spotify_connection():
    scope='user-read-currently-playing'
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )
    sp = spotipy.Spotify(auth_manager=sp_oauth)
    return sp

def get_track_info(track):
    if track:
        artist = track["item"]["artists"][0]["name"]
        song = track["item"]["name"]
        track_id = track["item"]["id"]
        return (artist, song, track_id)
    return None

def get_track_key(track_id):
    recco_beats_url = RECCO_BEATS_BASE_URL + track_id
    try:
        response = requests.get(recco_beats_url, timeout=5)
        response.raise_for_status()
        data = response.json()

        key_int = data["content"][0]["key"]
        key_mode = data["content"][0]["mode"]
        if key_mode == 0:
            key_int += 3
        key_str = RECCO_BEATS_KEY_MAP[key_int]

        return key_str
    except requests.RequestException as e:
        print(f"ReccoBeats request failed: {e}")
        return None
    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"Unexpected ReccoBeats response: {e}")
        return None


def main():
    sp = create_spotify_connection()

    previous_track_id = None
    current_track_id = None

    while True:
        current_track = sp.current_user_playing_track()
        current_track_info = get_track_info(current_track)

        if current_track_info is not None:
            artist, song, current_track_id = current_track_info

            if current_track_id != previous_track_id:
                print(f"Track changed to: {song} - {artist}")
                track_key = get_track_key(current_track_id)
                print(f"key: {track_key}")
                previous_track_id = current_track_id
            else:
                print("Track has not changed")

        else:
            print("No track currently playing")
            break

        time.sleep(5)

if __name__=="__main__":
    main()