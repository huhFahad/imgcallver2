#vol_control.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore import Qt


class VolumeControlWidget(QWidget):
    def __init__(self, media_manager, viewer):
        super().__init__()
        self.media_manager = media_manager
        self.viewer = viewer
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Volume Control")
        self.setStyleSheet("background-color: black; color: white;")

        # Layout
        layout = QVBoxLayout()

        # Background music volume control
        self.bg_label = QLabel("Background Music Volume")
        self.bg_slider = QSlider(Qt.Horizontal)
        self.bg_slider.setStyleSheet(self.slider_style())
        self.bg_slider.setRange(0, 100)
        self.bg_slider.setValue(self.viewer.bg_volume)
        self.bg_slider.valueChanged.connect(self.update_bg_volume)

        # Media audio volume control
        self.media_label = QLabel("Media Audio Volume")
        self.media_slider = QSlider(Qt.Horizontal)
        self.media_slider.setStyleSheet(self.slider_style())
        self.media_slider.setRange(0, 100)
        self.media_slider.setValue(self.viewer.media_volume)
        self.media_slider.valueChanged.connect(self.update_media_volume)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        # Add widgets to layout
        layout.addWidget(self.bg_label)
        layout.addWidget(self.bg_slider)
        layout.addWidget(self.media_label)
        layout.addWidget(self.media_slider)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

    def slider_style(self):
        return """
        QSlider {
            background-color: #f0f0f0;
            height: 10px;
            border-radius: 5px;
        }
        QSlider::handle {
            background-color: #0078d7;
            border: 2px solid #005a8a;
            border-radius: 5px;
            width: 20px;
            height: 20px;
        }
        QSlider::handle:pressed {
            background-color: #005a8a;
        }
        """

    def update_bg_volume(self):
        volume = self.bg_slider.value() / 100.0
        self.media_manager.background_channel.set_volume(volume)
        self.viewer.bg_volume = self.bg_slider.value()  # Save state
        print(f"Updated BG Volume to {volume}")

    def update_media_volume(self):
        volume = self.media_slider.value() / 100.0
        self.media_manager.media_channel.set_volume(volume)
        self.viewer.media_volume = self.media_slider.value()  # Save state
        print(f"Updated Media Volume to {volume}")
