# intro
This folder contains the Micropython libraries for **sdcard**, **urequest**, and **ssd1306**.

## SDcard
Saving for file, similar to how a USB driver work. 
In Micropython, the sdcard must be formatted in **FAT32** or **FAT16**, and the maximum supported size is **32GB**. 
If the card is not **FAT format** and **exceeds 32GB**, you need to format it to FAT32 or FAT16 using your computer.

## urequests
This Module similar to python frameworks like **FastAPI** or **Flask**, used to make HTTP requests (e.g. GET, POST).

## ssd1306
An I2C-based OLED diplay module.
It can display text or images in **black and white** on a small screan.
