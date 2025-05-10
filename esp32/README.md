# Intro
This file contains code that run on the Esp32, written in Micropython.

## `__init__`
This helps manager the file struct more easily.

## inital
This code initialize all the devices.

## I2S (Inter-IC Sound)
This module includes the microphone and audio player on Esp32, as described in detailed below.
### Intro
I2S (Inter-IC Sound) is a digital audio transmission standard primarily used for sending audio data between digital audio devices.   
It was developed by Philips in 1986 and is widely used in digital audio processing and playback devices.

### function
1. Digital Audio Transmission:
Used to transmit digital audio from one device to another, such as from a digital processer to a digital-to-analog converter (DAC)  
3. High Audio Quality
Support high-resolution audio data.

## I2C (Inter-Integrated Circuit)
I2C (Inter-Integrated Circuit) is a type of serial communication bus designed for internal integrated circuits.
It was developed by Philips in the 1980s to allow motherboards, mobile phones, and embedded systems to connect to low-speed peripheral devices.
I2C is mainly used for board-to-board communication and is not suitable for long-distance data transmission.  

However, the I2C bus can be applied in various control architectures, such as the System Management Bus (SMBus), Power Management Bus (PMBus), Intelligent Platform Management Interface (IPMI), Display Data Channel (DDC), and Advanced Telecom Computing Architecture (ATCA).  
information from 成大WIKI

## light
Controls LED open or closed.

## wifi
Connects wifi.

## connect_web 
Connect to backend of website, and can retrieving the data from backend, diplaying the picture and data analysis on I2C.
