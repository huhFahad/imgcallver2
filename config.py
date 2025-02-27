# config.py
import os, sys

class Config:
    API_GET_LATEST_PLAYLIST = "https://cloudbases.in/demoplatform/Robo/Robo_api/api_get_latest_playlist_id/1"
    API_GET_PLAYLIST = "https://cloudbases.in/demoplatform/Robo/Robo_api/api_get_playlist/"
    
    APP_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))
    DOWNLOADS_DIR = os.path.join(APP_DIR, "downloads")
    AUDIO_DIR = os.path.join(DOWNLOADS_DIR, "audio")
    IMAGES_DIR = os.path.join(DOWNLOADS_DIR, "images")
    BACKGROUND_MUSIC = os.path.join(DOWNLOADS_DIR, "Beat.mp3")
    BACKGROUND_IMAGE = os.path.join(DOWNLOADS_DIR, "centelonsolutions_logo.png")
    PLAYLIST_DATA = os.path.join(APP_DIR, "playlist_data.json")

    # Create necessary directories
    os.makedirs(AUDIO_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)