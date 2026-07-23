import random

import spotipy,os,time
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

class SpotifyController:
    def __init__(self,default_device_name = None):
        """
        Initializes a SpotifyController object that can be used to control Spotify playback. It sets up the Spotify client using the Spotipy library and authenticates using the SpotifyOAuth method with credentials provided in environment variables. If a default device name is provided, it will be used for playback; otherwise, the first available device will be used.
        Args:            default_device_name (str, optional): The name of the Spotify device to use for playback.
        """
        self.default_device_name = default_device_name
        client_id = os.getenv("client_id")
        client_secret = os.getenv("client_secret")
        redirect_uri = os.getenv("redirect_uri")
        print(client_id, client_secret, redirect_uri)
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="user-read-playback-state user-library-read playlist-read-private streaming user-modify-playback-state"
            )
        )

    def play(self, artist=None, track=None, playlist=None, device_name=None):
        if device_name:
                self.ensure_device_available(device_name)
                self.set_device_active(device_name)
        elif self.default_device_name:
                self.ensure_device_available(self.default_device_name)
                self.set_device_active(self.default_device_name)
        time.sleep(2) # Wait for the device to become active

        try:
            if playlist:
                playlist_uri = self.get_library_playlist(playlist)
                if not playlist_uri:
                    playlist_uri = self.sp.search(q=f"playlist:{playlist}", type="playlist", limit=1)["playlists"]["items"][0]["uri"]
                self.play_playlist(playlist_uri)
            elif track:
                track_uri = self.sp.search(q=f"track:{track} artist:{artist}" if artist else f"track:{track}", type="track", limit=1)["tracks"]["items"][0]["uri"]
                self.play_track(track_uri)
            elif artist:
                artist_uri = self.sp.search(q=f"artist:{artist}", type="artist", limit=1)["artists"]["items"][0]["uri"]
                self.play_artist(artist_uri)
            else:
                self.sp.start_playback()
              
        except spotipy.SpotifyException as e:
            return "ERREUR,",e
    
    def pause(self):
        try:    
            self.sp.pause_playback()
        except spotipy.SpotifyException as e:
            return "ERREUR,",e

    def play_track(self, track_uri):
        self.sp.start_playback(uris=[track_uri])

    def play_playlist(self, playlist_uri):
        playlist_id = playlist_uri.split(":")[-1]
        total_tracks = self.sp.playlist(playlist_id, fields="tracks.total")["tracks"]["total"]
        random_position = random.randint(0, total_tracks - 1) #this is done so it selects a random track from the playlist, while making sure the position given is within the range of the total number of tracks in the playlist

        self.sp.shuffle(True)
        self.sp.start_playback(context_uri=playlist_uri, offset={"position": random_position})

    def play_artist(self, artist_uri):
        self.sp.start_playback(context_uri=artist_uri)

    def play_album(self, album_uri):
        self.sp.start_playback(context_uri=album_uri)

    def set_device_active(self, device_name=None):
        devices = self.sp.devices()
        if devices["devices"]:
            if device_name:
                device_id = next((device["id"] for device in devices["devices"] if device["name"] == device_name), None)
            else:
                device_id = devices["devices"][0]["id"]
            if device_id:
                self.sp.transfer_playback(device_id=device_id, force_play=False)
                time.sleep(2) # Wait for the device to become active
        
    def set_repeat(self, state="track"):
        self.sp.repeat(state)

    def set_shuffle(self, state=True):
        self.sp.shuffle(state)

    def get_library_playlist(self, name):
        playlists = self.sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'].lower() == name.lower():
                return playlist['uri']
        return None
    
    def restart_raspotify(self):
        import subprocess
        subprocess.run(["sudo", "systemctl", "restart", "raspotify"],check=True)

    def ensure_device_available(self,device_name: str, retries: int = 2):
        for attempt in range(retries):
            devices = self.sp.devices()["devices"]
            for d in devices:
                if d["name"] == device_name:
                    return d["id"]  # found it, no restart needed
            print(f"Device not found (attempt {attempt + 1}), restarting raspotify...")
            self.restart_raspotify()
        raise RuntimeError(f"Could not find Spotify device '{device_name}' after {retries} restarts")