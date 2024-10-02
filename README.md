# color_detection

Project Overview: Real-Time Color Detection System
This project is a real-time color detection system designed to assist individuals in identifying various colors through a camera feed. It provides both visual and audio feedback whenever a specific color is detected. The system is developed using the following libraries and frameworks:

Libraries and Frameworks Used:
OpenCV (Open Source Computer Vision Library):

Purpose: OpenCV is used for capturing video frames from the webcam and performing color detection using image processing techniques.
Functionality: It allows converting images between different color spaces (e.g., BGR to HSV), creating color masks, and applying Gaussian blur to reduce noise in the image.
NumPy (Numerical Python):

Purpose: NumPy is used for handling arrays and performing mathematical operations on images.
Functionality: It helps in defining color ranges as arrays and applying logical operations to identify pixels that match specific color criteria.
PIL/Pillow (Python Imaging Library):

Purpose: Pillow is used to handle image conversions and compatibility with the Tkinter canvas.
Functionality: It allows the captured video frame to be converted from OpenCV's numpy format to an image format that can be displayed in the Tkinter GUI.
Tkinter:

Purpose: Tkinter is a built-in Python library used for creating the graphical user interface (GUI).
Functionality: It provides a canvas to display the video feed and buttons for controlling the detection process (start/stop detection, toggle audio feedback).
pyttsx3 (Text-to-Speech Conversion Library):

Purpose: This library enables the text-to-speech feature, providing audio feedback whenever a specific color is detected.
Functionality: It converts the detected color names into spoken words, which are output through the system’s audio device.
How the System Works:
The system captures live video frames from the webcam using OpenCV.
It converts the captured frames into HSV color space, where each pixel is compared against predefined color ranges using NumPy arrays.
If a color is detected in a specified region of interest (ROI), the system updates the GUI and provides audio feedback using pyttsx3.
The GUI, built with Tkinter, displays the real-time video feed and allows users to start/stop detection and toggle audio feedback.
