# gui.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QHBoxLayout, QPushButton, QStackedWidget, QApplication
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QTimer
from config import Config
from media_manager import MediaManager
from wifi_control import WiFiSettingsDialog, get_wifi_strength

class UpdateSignal(QObject):
    update_images = pyqtSignal(list)

class ImageViewer(QMainWindow):
    def __init__(self, media_manager):
        super().__init__()
        self.media_manager = media_manager
        self.setFixedSize(1920,1080)
        self.init_ui()
        self.bg_volume = 100  # Default background music volume 
        self.media_volume = 100  # Default media audio volume 
        self.wifi_update_timer = QTimer(self)  # Create a timer for periodic Wi-Fi checks
        self.wifi_update_timer.timeout.connect(self.update_wifi_status)  # Connect the timeout signal to the status update method
        self.wifi_update_timer.start(3000)  # Update every 5 seconds (adjust the interval as needed)


        
    def init_ui(self):
        self.setWindowTitle("Image Viewer")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.showFullScreen()

        self.widget = QWidget()
        self.layout = QVBoxLayout()
        self.widget.setStyleSheet("background-color: black;")

         # Add a persistent QLabel for image display
        self.image_widget = QLabel(self)
        self.image_widget.setAlignment(Qt.AlignCenter)
        self.image_widget.setScaledContents(True)
        self.layout.addWidget(self.image_widget)

        # # Create a stacked widget for images
        # self.stacked_widget = QStackedWidget()
        # self.image_widget = QLabel(self)
        # self.image_widget.setAlignment(Qt.AlignCenter)
        # self.stacked_widget.addWidget(self.image_widget)
        # self.layout.addWidget(self.stacked_widget)

        # Volume control button (added directly to layout)
        self.volume_button = QPushButton("", self)
        self.volume_button.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: white;
          
            border-radius: 20px;
            padding: 10px;
        }
        QPushButton:hover {
            background-color: #666;
        }
        QPushButton:pressed {
            background-color: #222;
        }
        """)  #border: 2px solid #888;
        
        # self.volume_button.setGeometry(10, 10, 150, 40)  # x, y, width, height
        
        vol_icon = QIcon("vol_icon.png")  # Provide the path to your icon image
        self.volume_button.setIcon(vol_icon)
        self.volume_button.setIconSize(QSize(30, 30))  # Adjust the icon size
        
        self.volume_button.setFixedSize(50, 50)  # Set width and height in pixels
        # self.volume_button.move(self.width() - 220, 20)  # Position: Top-right with margins
        self.volume_button.clicked.connect(self.open_volume_control)
        print("Volume button created and added to layout.")
        
        # Add a separate layout for positioning the button
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.volume_button)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)  # Position top-right

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        # Add Wi-Fi Settings Button
        self.wifi_button = QPushButton("", self)
        self.wifi_button.setStyleSheet("""
    QPushButton {
        background-color: white;
        color: white;
        
        border-radius: 20px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #666;
    }
    QPushButton:pressed {
        background-color: #222;
    }
""")# border: 2px solid #888;
           
        wifi_icon = QIcon("wifi_icon.png")  # Provide the path to your icon image
        self.wifi_button.setIcon(wifi_icon)
        self.wifi_button.setIconSize(QSize(30, 30))  # Adjust the icon size
        
        self.wifi_button.setFixedSize(50, 50)  # Set width and height in pixels
        self.wifi_button.clicked.connect(self.open_wifi_settings)
        button_layout.addWidget(self.wifi_button)

        # Signal for updating images
        self.signal = UpdateSignal()
        self.signal.update_images.connect(self.update_image_display)

        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def open_volume_control(self):
        self.volume_control = VolumeControlWidget(self.media_manager, self)
        screen_geometry = QApplication.desktop().screenGeometry()
        x = self.width() - self.volume_control.width() - 20  # 20px margin from the right
        y = 20  # 20px margin from the top
        self.volume_control.move(1700, 800)
        self.volume_control.show()
    
    def update_image_display(self, image_urls):
        
        # # Clear existing images
        # for i in reversed(range(self.layout.count())):
        #     widget = self.layout.itemAt(i).widget()
        #     if isinstance(widget, QLabel):  # Clears only QLabel widgets
        #         widget.setParent(None)
                
        if not image_urls:
            image_urls = [Config.BACKGROUND_IMAGE]
            
        # Add new images
        for url in image_urls:
            pixmap = self.load_image(url)
            if pixmap:
                # label = QLabel(self)
                pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                # label.setPixmap(pixmap)
                # label.setAlignment(Qt.AlignCenter)
                # label.setScaledContents(True)
                # self.layout.addWidget(label)

                # Ensure the pixmap isn't too large for the widget
                # Limit the pixmap size to avoid widget expansion
                max_width = self.width()  # Maximum width of the widget
                max_height = self.height()  # Maximum height of the widget
                
                # Scaling the pixmap to fit the maximum size
                pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio)


                self.image_widget.setPixmap(pixmap)
                self.image_widget.setAlignment(Qt.AlignCenter)
                self.image_widget.setScaledContents(True)

                 # Set the size of the image widget to be fixed based on the pixmap size
                self.image_widget.setFixedSize(pixmap.size())  # Set size based on pixmap's size

    def load_image(self, url):
        try:
            media_manager = MediaManager()
            local_path = media_manager.download_image(url)
            if local_path:
                return QPixmap(local_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            return QPixmap(Config.BACKGROUND_IMAGE)

    def open_wifi_settings(self):
        wifi_dialog = WiFiSettingsDialog()
        wifi_dialog.move(1300,500)
        wifi_dialog.exec_()

    def update_wifi_status(self):
        """Check Wi-Fi connection and update the Wi-Fi button"""
        connected, _ = get_wifi_strength(self)  # Check Wi-Fi connection status
        if connected:
            self.wifi_button.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    border-radius: 20px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QPushButton:pressed {
                    background-color: #222;
                }
            """)
        else:
            self.wifi_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border-radius: 20px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QPushButton:pressed {
                    background-color: #222;
                }
            """)


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
        self.bg_slider.setStyleSheet("""
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
""")
        self.bg_slider.setRange(0, 100)
        self.bg_slider.setValue(self.viewer.bg_volume)
        self.bg_slider.valueChanged.connect(self.update_bg_volume)

        # Media audio volume control
        self.media_label = QLabel("Media Audio Volume")
        self.media_slider = QSlider(Qt.Horizontal)
        self.media_slider.setStyleSheet("""
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
""")
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
