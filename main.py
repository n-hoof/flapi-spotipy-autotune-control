import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import requests
import time
from dataclasses import dataclass
from autotune_controls import set_up_flapi_connection, change_key

load_dotenv()

MAJOR_MODE = 1
MINOR_MODE = 0
RECCO_BEATS_URL = "https://api.reccobeats.com/v1/audio-features"
RECCO_BEATS_KEY_MAP = {
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
    11: "B"
}

@dataclass(frozen=True)
class Track:
    id: str
    name: str
    artist: str

def get_required_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}"
        )

    return value

def create_spotify_connection() -> spotipy.Spotify:
    sp_oauth = SpotifyOAuth(
        client_id=get_required_env("CLIENT_ID"),
        client_secret=get_required_env("CLIENT_SECRET"),
        redirect_uri=get_required_env("REDIRECT_URI"),
        scope="user-read-currently-playing"
    )

    return spotipy.Spotify(auth_manager=sp_oauth)

def get_current_track(sp: spotipy.Spotify) ->  Track | None:
    current_track = sp.current_user_playing_track()

    if not current_track:
        return None

    item = current_track.get("item")

    if not item or item.get("type") != "track":
        return None

    return Track(
        id = item["id"],
        name = item["name"],
        artist = item["artists"][0]["name"]
    )

def get_major_key(key_int: int, mode: int) -> str:
    #Convert minor keys to major
    if mode == MINOR_MODE:
        key_int = (key_int + 3) % 12

    return RECCO_BEATS_KEY_MAP[key_int]

def get_track_key(track_id: str, session: requests.Session) -> str | None:
    try:
        response = session.get(RECCO_BEATS_URL, params={"ids": track_id}, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        content = data["content"]
        
        if not content:
            return None

        key_int = content[0]["key"]
        key_mode = content[0]["mode"]

        return get_major_key(key_int, key_mode)
    
    except requests.RequestException as e:
        print(f"ReccoBeats request failed: {e}")
        return None
    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"Unexpected ReccoBeats response: {e}")
        return None


def main():
    sp = create_spotify_connection()
    http = requests.Session()

    if set_up_flapi_connection():

        previous_track_id = None

        while True:
            try:
                current_track = get_current_track(sp)

                if current_track is None:
                    print("No track currently playing")
                    break

                if current_track.id != previous_track_id:
                    print(f"Track changed to: {current_track.name} - {current_track.artist}")
                    track_key = get_track_key(current_track.id, http)

                    if track_key is None:
                        print(f"Key not found")

                    change_key(track_key)
                    previous_track_id = current_track.id

                time.sleep(5)

            except Exception:
                raise

        
if __name__=="__main__":
    main()