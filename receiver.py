import wifi
import socketpool
import usb_hid
from adafruit_hid.mouse import Mouse

# WiFi credentials
SSID = "Galaxy S26 BF6E"
PASSWORD = "SBarai@123"

print("Connecting to WiFi...")
wifi.radio.connect(SSID, PASSWORD)
print(f"Connected! IP Address: {wifi.radio.ipv4_address}")

# Create a socket pool
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)  # UDP socket

# Bind to a port (must match sender)
PORT = 12345
server.bind(("0.0.0.0", PORT))

print(f"Listening for data on port {PORT}...")

# Setup USB HID Mouse
mouse = Mouse(usb_hid.devices)

# Flex threshold for clicks
FLEX_THRESHOLD = 20000

# Floating-point array to store incoming data
data_array = [0.0] * 6  # ✅ Fixed-size array of 6 floats

while True:
    try:
        # ✅ Correctly receive and decode bytes data
        memory = bytearray(80)  # Buffer to store incoming data
        num_bytes, addr = server.recvfrom_into(memory)  # Read into buffer
        received_data = memory[:num_bytes].decode("utf-8").strip()  # Decode valid bytes
        print(f"Received from {addr}: {received_data}")  # Debug print

        # Ensure correct format (expecting 6 values)
        values = received_data.split(",")
        if len(values) != 6:
            print("⚠️ Error: Incorrect data format received.")
            continue

        # ✅ Store received values in the floating-point array
        try:
            data_array = list(map(float, values))  # Convert and store
        except ValueError:
            print("⚠️ Error: Data conversion failed.")
            continue

        # Extract values from the array
        move_x, move_y, flex1_val, flex2_val, flex3_val, smooth_z = map(int, data_array)

        # Handle Drag & Drop (All flex sensors bent)
        if flex1_val < FLEX_THRESHOLD and flex2_val < FLEX_THRESHOLD and flex3_val < FLEX_THRESHOLD:
            mouse.press(Mouse.LEFT_BUTTON)  # Hold left click
            print("🖱️ Object Selected (Mouse Click)")

        # Release Drag (All flex sensors relaxed)
        elif flex1_val > FLEX_THRESHOLD and flex2_val > FLEX_THRESHOLD and flex3_val > FLEX_THRESHOLD:
            mouse.release(Mouse.LEFT_BUTTON)
            print("🖱️ Object Dropped (Mouse Release)")

        # Handle Left Click
        elif flex1_val < FLEX_THRESHOLD:
            mouse.click(Mouse.LEFT_BUTTON)
            print("🖱️ Left Click!")

        # Handle Right Click
        elif flex2_val < FLEX_THRESHOLD:
            mouse.click(Mouse.RIGHT_BUTTON)
            print("🖱️ Right Click!")

        # Handle Mouse Movement
        if move_x != 0 or move_y != 0:
            mouse.move(x=move_y, y=-move_x)  # Invert Y-axis
            print(f"🖱️ Moving Cursor: X={move_y}, Y={-move_x}")

        print(f"Flex Sensor 1 Value: {flex1_val}")  # Debug print

    except Exception as e:
        print(f"⚠️ Socket error: {e}")


