import board
import busio
import adafruit_mpu6050
import analogio
import time
import math
import socketpool
import wifi

SSID = "Galaxy S26 BF6E"
PASSWORD = "SBarai@123"


# Connect to WiFi
wifi.radio.connect(SSID, PASSWORD)
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_DGRAM) 
print(f"Connected! IP Address: {wifi.radio.ipv4_address}")
# Send data to HID module (Second Pico)
HID_IP = "10.211.68.236"  # Adjust to match the IP of the second Pico W
HID_PORT = 12345

# Setup I2C for MPU6050
i2c = busio.I2C(board.GP1, board.GP0)  # SCL, SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

# Setup Flex Sensors as Analog Inputs
flex1 = analogio.AnalogIn(board.A0)
flex2 = analogio.AnalogIn(board.A1)
flex3 = analogio.AnalogIn(board.A2)

# Sensitivity and deadzone settings
FLEX_THRESHOLD = 20000
cursor_sensitivity = 3
deadzone = 0.3
smooth_factor = 0.2

last_x, last_y, last_z = 0, 0, 0

def read_flex(sensor):
    return sensor.value  # Returns a 16-bit analog value (0-65535)

def read_mpu():
    return mpu.acceleration  # Returns (x, y, z) acceleration values

while True:
    flex1_val = read_flex(flex1)
    flex2_val = read_flex(flex2)
    flex3_val = read_flex(flex3)
    ax, ay, az = read_mpu()

    # Apply deadzone
    ax = 0 if abs(ax) < deadzone else ax
    ay = 0 if abs(ay) < deadzone else ay
    az = 0 if abs(az) < deadzone else az

    # Apply smoothing
    smooth_x = (ax * smooth_factor) + (last_x * (1 - smooth_factor))
    smooth_y = (ay * smooth_factor) + (last_y * (1 - smooth_factor))
    smooth_z = (az * smooth_factor) + (last_z * (1 - smooth_factor))

    last_x, last_y, last_z = smooth_x, smooth_y, smooth_z

    # Convert to cursor movement
    move_x = int(smooth_x * cursor_sensitivity)
    move_y = int(smooth_y * cursor_sensitivity)
    print(f"{move_x},{move_y},{flex1_val},{flex2_val},{flex3_val},{smooth_z}") 
    # Pack and send data
    data = f"{move_x},{move_y},{flex1_val},{flex2_val},{flex3_val},{smooth_z}"
    server.sendto(data.encode(), (HID_IP, HID_PORT ))

    time.sleep(0.1)  # Short delay for stability
