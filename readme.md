OLED WAN Monitor for Raspberry Pi
Displays real-time data on a 1.3" SH1106 I2C OLED display:

🌐 WAN Latency (to 8.8.8.8) or shows "Down" if there's no internet

🌡️ CPU Temperature

🖧 LAN Client Count (via nmap scan)

Tested on Raspberry Pi 4B running Raspberry Pi OS (Bullseye).

🧰 Hardware Requirements
Raspberry Pi (4B recommended)

1.3" I2C OLED Display (SH1106, 128x64)

4 Jumper Wires

OLED to Raspberry Pi Wiring
OLED Pin	Raspberry Pi GPIO Pin
GND	Pin 6 (GND)
VCC	Pin 1 (3.3V)
SCL	Pin 5 (GPIO3 / SCL1)
SDA	Pin 3 (GPIO2 / SDA1)

⚙️ Software Setup
Start with a fresh Raspberry Pi OS and internet connection.

1. Enable I2C
Run:

bash
Copy
Edit
sudo raspi-config
Navigate to: Interface Options > I2C > Enable

Reboot when prompted.

2. Install Dependencies
bash
Copy
Edit
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-pil python3-dev i2c-tools nmap git -y
sudo pip3 install sh1106
(Optional) Verify I2C OLED detection:

bash
Copy
Edit
i2cdetect -y 1
You should see an address like 0x3c.

3. Clone the Repository
bash
Copy
Edit
cd ~
git clone https://github.com/gsrit/Raspberry-Pi-4B.git
cd 
chmod +x oled-display-rpi.py

4. Test the Script
bash
Copy
Edit
python3 oled-display-rpi.py
You should see:

WAN-10ms / Down

CPU - 30°C

LAN Clients - X

Press Ctrl+C to stop.

🚀 Auto-Start on Boot (systemd)
1. Create a Service File
bash
Copy
Edit
sudo nano /etc/systemd/system/oled-display.service
Paste this:

ini
Copy
Edit
[Unit]
Description=OLED Display WAN Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/YOUR_REPO_NAME/oled-display-rpi.py
WorkingDirectory=/home/pi/YOUR_REPO_NAME
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
✅ Update paths to match your setup.

2. Enable and Start the Service
bash
Copy
Edit
sudo systemctl daemon-reload
sudo systemctl enable oled-display.service
sudo systemctl start oled-display.service
Check if it’s running:

bash
Copy
Edit
sudo systemctl status oled-display.service
View logs:

bash
Copy
Edit
journalctl -u oled-display.service -e
🧪 Troubleshooting
Blank screen? Check wiring and run i2cdetect -y 1.

nmap crashes? Try nmap -sn --max-retries=1 --host-timeout=5s 192.168.X.0/24

Script exits silently? Isolate and run parts of the script manually.
