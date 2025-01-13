# playlist_manager.py

from config import Config
import requests
import json
import os

class PlaylistManager:
    def __init__(self):
        self.current_playlist_id = None
        
    def fetch_latest_playlist_id(self):
        try:
            response = requests.get(Config.API_GET_LATEST_PLAYLIST)
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("id")
        except Exception as e:
            print(f"Error fetching latest playlist ID: {e}")
            return None
            
    def fetch_media_list(self, playlist_id):
        try:
            response = requests.get(f"{Config.API_GET_PLAYLIST}{playlist_id}")
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("media_list", [])
        except Exception as e:
            print(f"Error fetching media list: {e}")
            return []
            
    def save_playlist_data(self, playlist_id, media_list):
        data = {
            "playlist_id": playlist_id,
            "media_list": media_list
        }
        
        with open(Config.PLAYLIST_DATA, "w") as f:
            json.dump(data, f)
            
    def load_playlist_data(self):

        if not os.path.exists(Config.PLAYLIST_DATA):  # Check if the file doesn't exist
            print("No playlist data file found, fetching playlist from server.")
            latest_id = self.fetch_latest_playlist_id()
            if latest_id:
                # Fetch the media list using the latest playlist ID
                media_list = self.fetch_media_list(latest_id)
                if media_list:
                    # Save the fetched playlist data to a file
                    self.save_playlist_data(latest_id, media_list)
                    return latest_id, media_list
            return None, None  # Return None if fetching fails

        try:
            with open(Config.PLAYLIST_DATA, "r") as f:
                data = json.load(f)
                return data["playlist_id"], data["media_list"]
        except Exception as e:
            print(f"Error loading playlist data: {e}")
            return None, None