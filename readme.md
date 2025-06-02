# OLED WAN Monitor for Raspberry Pi 4B

Displays real-time information on a 1.3" SH1106 I2C OLED display:

- **WAN Latency** to 8.8.8.8 (or shows "Down" if no internet)
- **CPU Temperature**
- **LAN Client Count** using `nmap`

Designed for Raspberry Pi 4B running Raspberry Pi OS (Bullseye or newer).

---

## Hardware Requirements

- Raspberry Pi 4B (or any model with I2C support)
- 1.3" I2C OLED Display (SH1106, 128x64)
- 4 Female-to-Female Jumper Wires

### Wiring: OLED to Raspberry Pi GPIO

| OLED Pin | Pi Pin | GPIO       | Description       |
|----------|--------|------------|-------------------|
| GND      | Pin 6  | GND        | Ground            |
| VCC      | Pin 1  | 3.3V       | Power             |
| SCL      | Pin 5  | GPIO3 (SCL)| I2C Clock         |
| SDA      | Pin 3  | GPIO2 (SDA)| I2C Data          |

---

## Software Installation (from scratch)

### 1. Enable I2C Interface

Run:

```bash
sudo raspi-config
```

Navigate to:  
`Interface Options` → `I2C` → Enable → Reboot when prompted.

---

### 2. Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-pil python3-dev i2c-tools nmap git
sudo pip3 install sh1106
```

To verify OLED is detected:

```bash
i2cdetect -y 1
```

You should see `3c` on the grid if connected correctly.

---

### 3. Clone This Repository

```bash
cd ~
git clone https://github.com/gsrit/Raspberry-Pi-4B.git
cd Raspberry-Pi-4B
chmod +x oled-display-rpi.py
```

---

### 4. Test the Script

```bash
python3 oled-display-rpi.py
```

Output will be shown on the OLED as:

```
WAN - 15ms / Down
CPU - 45°C
LAN Clients - 5
```

Stop with `Ctrl + C`.

---

## Auto-Run on Boot with systemd

### 1. Create a systemd Service File

```bash
sudo nano /etc/systemd/system/oled-display.service
```

Paste this (modify path if your username differs):

```ini
[Unit]
Description=OLED Display WAN Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Raspberry-Pi-4B/oled-display-rpi.py
WorkingDirectory=/home/pi/Raspberry-Pi-4B
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

---

### 2. Enable and Start the Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable oled-display.service
sudo systemctl start oled-display.service
```

Check if it works:

```bash
sudo systemctl status oled-display.service
```

See live logs:

```bash
journalctl -u oled-display.service -e
```

---

## Troubleshooting

- **Nothing on screen:** Check I2C wiring and run `i2cdetect -y 1`
- **Display flashes once and goes blank:** Likely a Python script issue or crash—check logs.
- **nmap crashes:** Use reduced scan options:
  ```bash
  nmap -sn --max-retries=1 --host-timeout=5s 192.168.111.0/24
  ```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

[gsrit](https://github.com/gsrit)
