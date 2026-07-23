import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id="c9b479bd1ac0453b8c18aadce7301a29",
                client_secret="99d43c1b8e7b4d80a7e26954fdd0fcd6",
                redirect_uri="https://10.0.0.17:8888/callback",
                scope="user-read-playback-state user-library-read playlist-read-private streaming user-modify-playback-state"
            ))
print(sp.devices())

