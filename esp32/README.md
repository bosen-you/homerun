# ESP32 MicroPython Project

This folder contains code written in **MicroPython** for the **ESP32** microcontroller. It includes modules for device initialization, I2S/I2C communication, Wi-Fi connection, and web backend interaction.

## File Overview

- `__init__.py`  
  Helps manage the folder as a Python package and organize file structure more effectively.

- `init.py`  
  Initializes all connected devices when the ESP32 starts.

- `i2s.py`  
  Handles I2S communication for microphone input and audio output.

- `i2c.py`  
  Manages I2C communication with peripherals like displays or sensors.

- `light.py`  
  Controls an LED—turning it on or off.

- `wifi.py`  
  Connects the ESP32 to a Wi-Fi network.

- `connect_web.py`  
  Connects to a web backend, retrieves data, displays images and performs data visualization using I2C-connected devices.

---

## I2S (Inter-IC Sound)

### Overview
I2S is a digital audio transmission standard used for transferring audio between digital devices. Developed by Philips in 1986, it's commonly used in modern audio systems for its support of high-resolution audio.

### Features
1. **Digital Audio Transmission** – Transfers audio from devices like a digital signal processor (DSP) to a digital-to-analog converter (DAC).  
2. **High Audio Quality** – Supports high-resolution audio formats.

---

## I2C (Inter-Integrated Circuit)

### Overview
I2C is a serial communication protocol designed for communication between integrated circuits. It is commonly used for short-distance communication in embedded systems.

### Applications
- Display Data Channel (DDC)
- System Management Bus (SMBus)
- Power Management Bus (PMBus)
- IPMI and ATCA platforms

*Source: NCKU Wiki*

---

## Wi-Fi & Web Integration

This project also connects the ESP32 to a backend server via Wi-Fi, allowing real-time data fetching and displaying the results (including images) through an I2C-connected screen or other peripherals.
