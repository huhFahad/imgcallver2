import subprocess
import platform
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox

class WiFiSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Wi-Fi Settings")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.network_list = QListWidget()
        layout.addWidget(self.network_list)

        connect_button = QPushButton("Connect")
        connect_button.clicked.connect(self.connect_to_wifi)
        layout.addWidget(connect_button)

        self.setLayout(layout)
        self.populate_wifi_networks()

    def populate_wifi_networks(self):
        """Fetch available Wi-Fi networks and populate the list based on OS."""
        try:
            if platform.system() == "Windows":
                # Check if there is a wireless adapter
                result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True)
                if result.returncode != 0:
                    QMessageBox.warning(self, "Error", "No wireless adapter found or access denied.")
                    return

                # List available Wi-Fi networks
                result = subprocess.check_output(["netsh", "wlan", "show", "network"])
                networks = []
                for line in result.decode().splitlines():
                    if "SSID" in line:
                        ssid = line.split(":")[1].strip()
                        networks.append(ssid)
                self.network_list.addItems(networks)

            elif platform.system() == "Linux":
                # List available Wi-Fi networks
                result = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "device", "wifi", "list"])
                networks = result.decode().strip().split("\n")
                self.network_list.addItems(networks)

            else:
                QMessageBox.warning(self, "Error", "Unsupported operating system.")
                return

        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to fetch Wi-Fi networks: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")

    def connect_to_wifi(self):
        """Connect to the selected Wi-Fi network."""
        selected_network = self.network_list.currentItem()
        if selected_network is None:
            QMessageBox.warning(self, "Error", "Please select a network.")
            return

        ssid = selected_network.text()

        try:
            if platform.system() == "Windows":
                # Connect to the Wi-Fi network using netsh (Windows)
                subprocess.run(["netsh", "wlan", "connect", ssid], check=True)

            elif platform.system() == "Linux":
                # Connect to the Wi-Fi network using nmcli (Linux)
                subprocess.run(["nmcli", "dev", "wifi", "connect", ssid], check=True)

            QMessageBox.information(self, "Success", f"Connected to {ssid}")
            self.close()
            
        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"Failed to connect: {e}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")
