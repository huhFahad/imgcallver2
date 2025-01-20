# gui.py
from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QSlider, QHBoxLayout, QPushButton, QStackedWidget, QApplication
from PyQt5.QtGui import QPixmap, QIcon, QMouseEvent
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QSize, QTimer
from config import Config
from media_manager import MediaManager
from wifi_control import WiFiSettingsDialog, get_wifi_strength
from vol_control import VolumeControlWidget
from screeninfo import get_monitors

class UpdateSignal(QObject):
    update_images = pyqtSignal(list)

class ImageViewer(QMainWindow):
    def __init__(self, media_manager):
        super().__init__()

        display_resolution = get_monitors()[0]  # Get the first monitor (if you have multiple, you can iterate)
        self.media_manager = media_manager
        self.setFixedSize(display_resolution.width,display_resolution.height)
        self.init_ui()
        self.bg_volume = 100  # Default background music volume 
        self.media_volume = 100  # Default media audio volume 
        
        self.wifi_update_timer = QTimer(self)  # Create a timer for periodic Wi-Fi checks
        self.wifi_update_timer.timeout.connect(self.update_wifi_status)  # Connect the timeout signal to the status update method
        self.wifi_update_timer.start(3000)  # Update every 5 seconds (adjust the interval as needed)

        self.last_mouse_position = None
        
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

        # Volume control button (added directly to layout)
        self.volume_button = QPushButton("", self)

        vol_icon = QIcon("icons/vol_icon.png")  # Provide the path to your icon image
        self.volume_button.setIcon(vol_icon)
        self.volume_button.setIconSize(QSize(30, 30))  # Adjust the icon size

        self.volume_button.setStyleSheet("""
        QPushButton {
            
            background-color: rgba(255,255,255,100%);
            color: white;
            border-radius: 20px;
            padding: 10px;
            
        }
        QPushButton:hover {
            
            background-color: rgba(200,200,255,100%);
            
        }
        QPushButton:pressed {
            
            background-color: #222;
            
        }
        """)  #border: 2px solid #888;
        
        # self.volume_button.setGeometry(10, 10, 150, 40)  # x, y, width, height
              
        self.volume_button.setFixedSize(50, 50)  # Set width and height in pixels
        # self.volume_button.move(self.width() - 220, 20)  # Position: Top-right with margins
        self.volume_button.clicked.connect(self.open_volume_control)
        
        # Add a separate layout for positioning the button
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.volume_button)
        button_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)  # Position top-right

        # Add the button layout to the main layout
        self.layout.addLayout(button_layout)

        # Add Wi-Fi Settings Button
        self.wifi_button = QPushButton("", self)

        wifi_icon = QIcon("icons/wifi_icon.png")  # Provide the path to your icon image
        self.wifi_button.setIcon(wifi_icon)
        self.wifi_button.setIconSize(QSize(30, 30))  # Adjust the icon size

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
                   
        self.wifi_button.setFixedSize(50, 50)  # Set width and height in pixels
        self.wifi_button.clicked.connect(self.open_wifi_settings)
        button_layout.addWidget(self.wifi_button)

        self.volume_button.setVisible(False)
        self.wifi_button.setVisible(False)

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
        if not image_urls:
            image_urls = [Config.BACKGROUND_IMAGE]
            
        # Add new images
        for url in image_urls:
            pixmap = self.load_image(url)
            if pixmap:
                pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

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
                    opacity: 0.5;
                }
                QPushButton:hover {
                    background-color: #666;
                    opacity: 1.0;
                }
                QPushButton:pressed {
                    background-color: #222;
                    opacity: 1.0;
                }
            """)
        else:
            self.wifi_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border-radius: 20px;
                    padding: 10px;
                    opacity: 0.5;
                }
                QPushButton:hover {
                    background-color: #666;
                    opacity: 1.0;
                }
                QPushButton:pressed {
                    background-color: #222;
                    opacity: 1.0;
                }
            """)

    def mouseMoveEvent(self, event: QMouseEvent):
        # Detect mouse movement anywhere on the screen
        pos = event.pos()
        if self.last_mouse_position is None:
            self.last_mouse_position = pos

        # If the mouse has moved, you can handle it as needed
        if pos != self.last_mouse_position:
            print(f"Mouse moved to: {pos}")
            self.last_mouse_position = pos

    def enterEvent(self, event):
        # This is triggered when the mouse enters the window
        print("Mouse entered the window.")
        self.show_buttons()

    def leaveEvent(self, event):
        # This is triggered when the mouse leaves the window
        print("Mouse left the window.")
        self.hide_buttons()

    def show_buttons(self):
        # Show the buttons when the mouse enters the window
        if not self.volume_button.isVisible():
            self.volume_button.setVisible(True)
            print("Volume button is now visible.")

        if not self.wifi_button.isVisible():
            self.wifi_button.setVisible(True)
            print("Wi-Fi button is now visible.")

        # Set a timer to hide the buttons after 3 seconds
        QTimer.singleShot(3000, self.hide_buttons)

    def hide_buttons(self):
        # Hide the buttons
        if self.volume_button.isVisible():
            self.volume_button.setVisible(False)
            print("Volume button is now hidden.")

        if self.wifi_button.isVisible():
            self.wifi_button.setVisible(False)
            print("Wi-Fi button is now hidden.")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            print("Left mouse button clicked at:", event.pos())