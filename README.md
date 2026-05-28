# POINTICK
This project implements a wireless glove-based mouse that allows users to control a computer cursor using hand gestures, flex sensors, and an IMU (accelerometer + gyroscope). The system consists of two Raspberry Pi Pico W devices on gloves and a third Pico W acting as a base station that transmits data to the computer via USB HID. 

## Project Overview
This project is a wireless glove-based mouse that replaces traditional pointing devices with hand gestures.
Users can move the cursor, click, drag, and scroll using hand movements and flex sensor inputs.

- **Hand Glove**: Controls mouse movement, clicks, drag and drop function and handles scrolling.
- **Base Station**: Combines data and sends it to the computer via USB HID.

## Hardware Requirements
- **Hand Glove**:


  - 1 Raspberry Pi Pico W
  - 3 Flex Sensors (Index & Middle Finger)
  - MPU6050 (Accelerometer + Gyroscope)
  - A 3.3V Battery (Alternatively using another battery with a suitable buck convertor)
  - A battery holder
  - a perfboard
  - 10 kilo ohm resistors
  - Singlecore wires (22AWG) (for making connections in perf board)
  - (Alternatively, u can also make use of jumper wires and a mini breadboard)

- **Base Station**:

  - 1 Raspberry Pi Pico W
  - 1 USB Connection to PC

 <img width="1280" height="960" alt="Pointick" src="https://github.com/user-attachments/assets/531aac3f-bba0-4a76-b308-8a7350e84670" />

 

