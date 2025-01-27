# media_manager.py
import requests, os, pygame
from config import Config

class MediaManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_channel = pygame.mixer.Channel(0)
        self.media_channel = pygame.mixer.Channel(1)
        # self.vol_control_widget = VolumeControlWidget(self.media_manager, viewer)
        
    def download_file(self, url, directory):
        try:

            # If the URL is actually a local path, return it as is
            if os.path.exists(url):
                return url

            filename = os.path.join(directory, url.split("/")[-1])
            if os.path.exists(filename):
                return filename
                
            response = requests.get(url)
            response.raise_for_status()
            
            with open(filename, "wb") as f:
                f.write(response.content)
            
            return filename
        except Exception as e:
            print(f"Error downloading file from {url}: {e}")
            return None
            
    def download_audio(self, url):
        return self.download_file(url, Config.AUDIO_DIR)
        
    def download_image(self, url):
        return self.download_file(url, Config.IMAGES_DIR)
        
    def play_audio(self, audio_url, background_volume=0.2):
        try:
            filename = self.download_audio(audio_url)
            if not filename:
                return 0
                
            sound = pygame.mixer.Sound(filename)
            
            # Lower background music volume
            self.background_channel.set_volume(background_volume)
            
            # Play media audio
            self.media_channel.play(sound)
            
            return sound.get_length()
        except Exception as e:
            print(f"Error playing audio: {e}")
            return 0
            
    def play_background_music(self):
        if os.path.exists(Config.BACKGROUND_MUSIC):
            background_sound = pygame.mixer.Sound(Config.BACKGROUND_MUSIC)
            self.background_channel.play(background_sound, loops=-1)
            # volume = self.vol_control_widget.bg_slider.value() / 100.0
            self.background_channel.set_volume(0.69)
            
    def restore_background_volume(self,v):
        self.background_channel.set_volume(v)
        print(f"Restored to {v}")