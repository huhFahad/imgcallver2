#!/usr/bin/env python3
# main.py

import sys, subprocess, time, pygame
from threading import Thread
from PyQt5.QtWidgets import QApplication
from gui import ImageViewer
from vol_control import VolumeControlWidget
from media_manager import MediaManager
from playlist_manager import PlaylistManager
from config import Config

class PlaylistMonitor(Thread):
    def __init__(self, viewer, interval=2):
        super().__init__()
        self.viewer = viewer
        self.interval = interval
        self.running = True
        self.media_manager = MediaManager()
        self.playlist_manager = PlaylistManager()
        self.vol_control_widget = VolumeControlWidget(self.media_manager, viewer)
        
    def run(self):
        """Main thread loop that checks for new playlists"""
        
        try:
            # Only start the background music once
            if not hasattr(self, 'background_playing') or not self.background_playing:
                self.media_manager.play_background_music()  # Start background music
                self.background_playing = True  # Flag to avoid resetting background music

            # Load or fetch playlist
            current_id, media_list = self.playlist_manager.load_playlist_data()
            latest_id = self.playlist_manager.fetch_latest_playlist_id()
                            
            print("LOOP TEST")

            # If no playlist data available or no network, display default image and continue playing bg music
            if not media_list:
                print("No playlist available, displaying default image")
                image_urls = [Config.BACKGROUND_IMAGE]
                self.viewer.signal.update_images.emit(image_urls)
                time.sleep(self.interval)  # Sleep and continue checking periodically
                return  # Skip the rest of the loop
            
            if latest_id and latest_id != current_id:
                media_list = self.playlist_manager.fetch_media_list(latest_id)
                self.playlist_manager.save_playlist_data(latest_id, media_list)
                
            if media_list:
                self.play_media_list(media_list)
                
        except Exception as e:
            print(f"Error in monitoring: {e}")
            pass

        # Continue checking for new playlists every interval (in seconds)
        if self.running:
            time.sleep(self.interval)
            self.run()  # Recursively call run to keep the thread going

    def play_media_list(self, media_list):
        """Play through each media set once"""
        for media in media_list:
            try:
                image_urls = media.get("images", []) 
                audio_url = media.get("audio", "")
                
                if not image_urls and not audio_url:
                    print("Skipping media set with missing image or audio")
                    
                
                # Download audio file first to ensure it's ready
                audio_file = self.media_manager.download_audio(audio_url)
                if not audio_file:
                    print(f"Failed to download audio: {audio_url}")
                    continue
                
                # Get audio duration
                sound = pygame.mixer.Sound(audio_file)
                audio_duration = sound.get_length()
                
                # Display image
                print(f"Displaying image from set with audio: {audio_url}")
                self.viewer.signal.update_images.emit(image_urls)
                
                # Wait 1 second before starting audio
                time.sleep(1)
                
                # Play audio
                print(f"Playing audio: {audio_url}")
                self.media_manager.play_audio(audio_url)
                
                # Wait for audio duration plus 3 seconds
                total_wait = audio_duration + 3
                time.sleep(total_wait)
                
                # Restore background music volume
                # self.vol_control_widget.update_bg_volume()
                volume = self.vol_control_widget.bg_slider.value() / 100.0
                self.media_manager.restore_background_volume(volume)
                print(f"inside main vol = {volume}")
                
                
            except Exception as e:
                print(f"Error playing media set: {e}")
                continue
    
    def stop(self):
        """Stop the monitor thread"""
        self.running = False

def set_hdmi_as_default():
    try:
        # List all sinks to find the HDMI output
        sinks = subprocess.check_output(["pactl", "list", "short", "sinks"]).decode()
        
        # Look for the sink related to HDMI
        hdmi_sink = None
        for line in sinks.splitlines():
            if "hdmi" in line.lower():
                hdmi_sink = line.split("\t")[1]
                break

        if not hdmi_sink:
            print("HDMI audio output not found.")
            return

        # Set the HDMI sink as default
        subprocess.run(["pactl", "set-default-sink", hdmi_sink], check=True)

        # Move all currently playing audio streams to the HDMI sink
        streams = subprocess.check_output(["pactl", "list", "short", "sink-inputs"]).decode()
        for line in streams.splitlines():
            stream_id = line.split("\t")[0]
            subprocess.run(["pactl", "move-sink-input", stream_id, hdmi_sink], check=True)

        print(f"Default audio output set to: {hdmi_sink}")

    except subprocess.CalledProcessError as e:
        print(f"Error running pactl commands: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def suspend_screensaver(window):
    """Suspend screensaver for the given window."""
    window_id = int(window.winId())  # Get the Window ID
    subprocess.call(["xdg-screensaver", "suspend", str(window_id)])

def restore_screensaver(window):
    """Restore screensaver for the given window."""
    window_id = int(window.winId())  # Get the Window ID
    subprocess.call(["xdg-screensaver", "activate", str(window_id)])

def main():
    # set_hdmi_as_default()
    app = QApplication(sys.argv)
    media_manager = MediaManager()  # Instantiate MediaManager
    viewer = ImageViewer(media_manager) 
    viewer.show()

    suspend_screensaver(viewer)

    monitor = PlaylistMonitor(viewer)
    
    def run_playlist_loop():
        monitor.daemon = True
        monitor.start()
        # monitor.join()  # Wait for the playlist to finish
        
        # Monitor is now running indefinitely, so the main thread can be used for other things
        app.exec()
    
    # Start the playlist loop in a separate thread
    playlist_thread = Thread(target=run_playlist_loop, daemon=True)
    playlist_thread.start()
  
    app.aboutToQuit.connect(lambda: setattr(playlist_thread, "running", False))

    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()