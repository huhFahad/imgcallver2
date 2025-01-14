# import subprocess
# import platform
# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox

# class WiFiSettingsDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Wi-Fi Settings")
#         self.setFixedSize(400, 300)
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         self.network_list = QListWidget()
#         layout.addWidget(self.network_list)

#         connect_button = QPushButton("Connect")
#         connect_button.clicked.connect(self.connect_to_wifi)
#         layout.addWidget(connect_button)

#         self.setLayout(layout)
#         self.populate_wifi_networks()

#     def populate_wifi_networks(self):
#         """Fetch available Wi-Fi networks and populate the list based on OS."""
#         try:
#             # if platform.system() == "Windows":
#             #     # Check if there is a wireless adapter
#             #     self.result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True)
#             #     if self.result.returncode != 0:
#             #         QMessageBox.warning(self, "Error", "No wireless adapter found or access denied.")
#             #         return

#             #     # List available Wi-Fi networks
#             #     self.result = subprocess.check_output(["netsh", "wlan", "show", "network"])
#             #     networks = []
#             #     for line in self.result.decode().splitlines():
#             #         if "SSID" in line:
#             #             ssid = line.split(":")[1].strip()
#             #             networks.append(ssid)
#             #     self.network_list.addItems(networks)

#             if platform.system() == "Linux":
#                 # List available Wi-Fi networks
#                 self.result = subprocess.check_output(["nmcli", "-t", "-f", "SSID", "device", "wifi", "list"])
#                 networks = self.result.decode().strip().split("\n")
#                 self.network_list.addItems(networks)

#             else:
#                 QMessageBox.warning(self, "Error (populate_wifi_networks > OS else)", "Unsupported operating system.")
#                 return

#         except subprocess.CalledProcessError as e:
#             QMessageBox.warning(self, "Error (populate_wifi_networks > subprocess.CalledProcessError)", f"Failed to fetch Wi-Fi networks: {e}")
#         except Exception as e:
#             QMessageBox.warning(self, "Error (populate_wifi_networks > Exception)", f"An unexpected error occurred: {e}")

#     def connect_to_wifi(self):
#         """Connect to the selected Wi-Fi network."""
#         selected_network = self.network_list.currentItem()
#         if selected_network is None:
#             QMessageBox.warning(self, "Error (connect_to_wifi > selected_network is None)", "Please select a network.")
#             return

#         ssid = selected_network.text()

#         try:
#             # if platform.system() == "Windows":
#             #     # Connect to the Wi-Fi network using netsh (Windows)
#             #     subprocess.run(["netsh", "wlan", "connect", ssid], check=True)

#             #     # Check if the connection was successful by verifying the active network
#             #     if self.result.returncode == 0:
#             #         # Verify if connected to the network
#             #         connection_check = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SSID", "device", "wifi", "list"])
#             #         if ssid in connection_check.decode():
#             #             QMessageBox.information(self, "Success", f"Connected to {ssid}")
#             #             self.close()
#             #         else:
#             #             QMessageBox.warning(self, "Error", f"Failed to connect to {ssid}.")
#             #     else:
#             #         QMessageBox.warning(self, "Error", f"Failed to connect to {ssid}.")

#             if platform.system() == "Linux":
#                 # Connect to the Wi-Fi network using nmcli (Linux)
#                 result = subprocess.run(["nmcli", "dev", "wifi", "connect", ssid], check=True)

#                 # Verify if connected to the network
#                 connection_check = subprocess.check_output(["nmcli", "-t", "-f", "ACTIVE,SSID", "device", "wifi", "list"])
#                 if f"yes:{ssid}" in connection_check.decode():
#                     QMessageBox.information(self, "Success", f"Connected to {ssid}")
#                 else:
#                     QMessageBox.warning(self, "Error", f"Failed to verify connection to {ssid}.")

#             else:
#                 QMessageBox.warning(self, "Error", "Unsupported operating system.")
#                 return
            
#         except subprocess.CalledProcessError as e:
#             QMessageBox.warning(self, "Error (connect_to_wifi > subprocess.CalledProcessError)", f"Failed to connect: {e}")
#         except Exception as e:
#             QMessageBox.warning(self, "Error (connect_to_wifi > Exception)", f"An unexpected error occurred: {e}")





import subprocess
import time
 
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from comm.message_box import show_message
 
class WifiDialog(QDialog):
    def __init__(self):
        super().__init__()
 
        try:
            subprocess.check_output(['nmcli', 'radio', 'wifi', 'on'], text=True)
            show_message(self, "Warning", "Please wait.. Scanning for available Wifi Networks...")
        except subprocess.CalledProcessError as e:
            show_message(self, "Error", f"Error enabling Wi-Fi: {e}")
 
        self.setWindowTitle('Wi-Fi Networks')
        self.setFixedSize(450, 300)
 
        # Wi-Fi network label and dropdown
        self.network_label = QLabel('Available Wi-Fi Networks:')
        self.network_label.setStyleSheet("font-size: 24px; font-weight: bold;")
 
        self.network_dropdown = QComboBox()
        self.network_dropdown.setPlaceholderText("Select a Wi-Fi network")
        self.network_dropdown.setStyleSheet("font: Roboto; color: black; background-color: rgb(220,220,220); font-weight: 500; font-size: 22px; padding-left: 10px;")
        self.network_dropdown.setFixedHeight(50)
 
        self.populate_wifi_networks(100)
 
        self.password_label = QLabel('Password:')
        self.password_label.setStyleSheet("font-size: 24px; font-weight: bold;")
 
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("font: Roboto; color: black; background-color: rgb(220,220,220); font-weight: 500; padding-left: 10px; font-size: 22px;")
        self.password_input.setFixedHeight(50)
#
        # Buttons for actions
        self.connect_button = QPushButton('Connect')
        self.connect_button.setStyleSheet("""
            QPushButton {color: black; background-color: rgba(210, 210, 222, 0.5); font-weight: bold; font-size: 20px;}
            QPushButton:pressed {background-color: rgba(210, 210, 222, 0.85); color: white; font-size: 20px;}
        """)
        self.connect_button.setFixedHeight(50)
        self.connect_button.clicked.connect(self.connect_to_wifi)
 
        self.disconnect_button = QPushButton('Disconnect')
        self.disconnect_button.setStyleSheet("""
            QPushButton {color: black; background-color: rgba(210, 210, 222, 0.5); font-weight: bold; font-size: 20px;}
            QPushButton:pressed {background-color: rgba(210, 210, 222, 0.85); color: white; font-size: 20px;}
        """)
        self.disconnect_button.setFixedHeight(50)
        self.disconnect_button.clicked.connect(self.disconnect_wifi)
 
        self.close_button = QPushButton('Close')
        self.close_button.setStyleSheet("""
            QPushButton {color: white; background-color: rgba(240, 0, 10, 0.7); font-size: 22px; font-weight: bold;}
            QPushButton:pressed {background-color: rgba(180, 0, 0, 0.85); border-style: inset; color: white;}
        """)
        self.close_button.setFixedHeight(50)
        self.close_button.clicked.connect(self.close)
 
        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.network_label)
        layout.addWidget(self.network_dropdown)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.connect_button)
        button_layout.addWidget(self.disconnect_button)
        button_layout.addWidget(self.close_button)
        layout.addStretch(1)
        layout.addLayout(button_layout)
        self.setLayout(layout)
 
    def populate_wifi_networks(self, num=3):
        """ Populate the available Wi-Fi networks in the dropdown """
        self.network_dropdown.clear()
        
        networks = self.scan_wifi_networks()
        
        if networks:
            self.network_dropdown.addItems(networks)
        elif num > 0:
            show_message(self, "Warning", "Please wait.. Scanning for available Wifi Networks...")
            time.sleep(2)  # Brief pause between scans
            self.populate_wifi_networks(num - 1)
        else:
            show_message(self, "Error", "No Wi-Fi networks detected after multiple attempts")
            self.close()
 
    def scan_wifi_networks(self):
        """ Use 'nmcli' to scan for available Wi-Fi networks and return a list of unique SSIDs """
        try:
            result = subprocess.check_output(
                ['nmcli', '-t', '-f', 'SSID,SECURITY,SIGNAL', 'device', 'wifi'], text=True
            )
            networks = {}
            for line in result.strip().split('\n'):
                if line:
                    fields = line.split(":")
                    ssid = fields[0].strip()  # SSID
                    security = fields[1].strip() if len(fields) > 1 else "Open"  # Security
                    signal = fields[2].strip() if len(fields) > 2 else "0"  # Signal Strength
 
                    if ssid and (ssid not in networks or int(signal) > int(networks[ssid]['signal'])):
                        networks[ssid] = {'security': security, 'signal': signal}
 
            return [
                f"{ssid} ({details['security']}, Signal: {details['signal']})"
                for ssid, details in networks.items()
            ]
 
        except subprocess.CalledProcessError as e:
            show_message(self, "Error", f"Failed to scan Wi-Fi networks. Command error: {e.stderr}")
        except Exception as e:
            show_message(self, "Error", f"Unexpected error while scanning Wi-Fi networks: {e}")
 
    def connect_to_wifi(self):
        try:
            full_ssid = self.network_dropdown.currentText()
            ssid = full_ssid.split(' (')[0]
            password = self.password_input.text()
 
            if not ssid or not password:
                show_message(self, "Error", "Please select a Wi-Fi network and enter a password")
                return
 
            result = subprocess.run(
                ['nmcli', 'device', 'wifi', 'connect', ssid, 'password', password],
                capture_output=True,
                text=True,
                timeout=15
            )
 
            if result.returncode == 0:
                show_message(self, "Success", f"Connected to {ssid}")
            else:
                error_message = result.stderr or result.stdout
                show_message(self, "Connection Error", f"Failed to connect to {ssid}:\n{error_message}")
 
        except subprocess.TimeoutExpired:
            show_message(self, "Error", "Connection attempt timed out")
        except Exception as e:
            show_message(self, "Error", f"Unexpected connection error: {e}")
 
 
    def disconnect_wifi(self):
        try:
            subprocess.check_output(['nmcli', 'radio', 'wifi', 'off'], text=True)
            show_message(self, "Disconnected", "Wi-Fi has been turned off.")
            self.close()
        except subprocess.CalledProcessError as e:
            show_message(self, "Error", f"Failed to disconnect Wi-Fi. Command error: {e.stderr}")
        except Exception as e:
            show_message(self, "Error", f"Unexpected error while disconnecting Wi-Fi: {e}")
 
 
 
def get_wifi_strength():
    """ Get the signal strength of the currently connected Wi-Fi network """
    try:
        # Call nmcli to get details of the active Wi-Fi connection
        result = subprocess.check_output(
            ['nmcli', '-t', '-f', 'IN-USE,SSID,SIGNAL', 'device', 'wifi'], text=True
        )
        
        # Process each line of the output
        for line in result.strip().split('\n'):
            if line.startswith('*'):  # The '*' indicates the currently active connection
                parts = line.split(':')
                if len(parts) >= 3:
                    ssid = parts[1].strip()  # The SSID
                    signal_strength = parts[2].strip()  # The Signal strength
                    # print(f"Connected to {ssid} with signal strength: {signal_strength}%")
                    return int(signal_strength)  # Convert signal strength to integer
        
        # Return None if no active connection found
        print("No active Wi-Fi connection detected.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None