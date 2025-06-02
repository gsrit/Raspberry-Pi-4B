from PIL import Image, ImageDraw, ImageFont
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
import time, subprocess

# Setup OLED
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)
width = device.width
height = device.height
font = ImageFont.load_default()

def get_ping_latency():
    try:
        result = subprocess.run(["ping", "-c", "1", "-W", "1", "8.8.8.8"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "time=" in line:
                    latency = line.split("time=")[-1].split(" ")[0]
                    return f"{latency} ms"
        return "Down"
    except:
        return "Down"

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp = int(f.read()) / 1000
        return f"{temp:.1f}°C"
    except:
        return "N/A"

def get_lan_clients():
    try:
        result = subprocess.check_output("nmap -sn 192.168.111.0/24 | grep 'Nmap scan report' | wc -l", shell=True)
        return result.decode().strip()
    except:
        return "N/A"

try:
    while True:
        # Create blank image for drawing.
        image = Image.new("1", (width, height))
        draw = ImageDraw.Draw(image)

        # Fetch data
        wan = get_ping_latency()
        temp = get_cpu_temp()
        clients = get_lan_clients()

        # Draw text
        draw.text((0, 0), f"WAN: {wan}", font=font, fill=255)
        draw.text((0, 16), f"CPU: {temp}", font=font, fill=255)
        draw.text((0, 32), f"LAN: {clients}", font=font, fill=255)

        # Send image to display
        device.display(image)
        time.sleep(1)

except KeyboardInterrupt:
    device.clear()
