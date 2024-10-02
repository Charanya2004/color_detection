import cv2
import numpy as np
import pyttsx3
import threading
from tkinter import *
from PIL import Image, ImageTk

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

# Define color ranges in HSV
color_ranges = {
    'Red': [(0, 100, 100), (10, 255, 255)],
    'Dark Red': [(160, 100, 100), (180, 255, 255)],
    'Green': [(35, 100, 100), (85, 255, 255)],
    'Light Green': [(25, 50, 50), (95, 255, 255)],
    'Blue': [(90, 50, 50), (130, 255, 255)],
    'Light Blue': [(80, 100, 100), (100, 255, 255)],
    'Yellow': [(20, 100, 100), (30, 255, 255)],
    'Orange': [(10, 100, 20), (25, 255, 255)],
    'Cyan': [(80, 100, 100), (100, 255, 255)],
    'Magenta': [(140, 100, 100), (160, 255, 255)],
    'Purple': [(130, 100, 100), (160, 255, 255)],
    'Pink': [(160, 50, 50), (180, 255, 255)],
    'Brown': [(10, 100, 20), (20, 255, 200)],
    'Gray': [(0, 0, 50), (180, 20, 200)],
    'Black': [(0, 0, 0), (180, 255, 30)],
    'White': [(0, 0, 200), (180, 20, 255)],
    'Lime': [(35, 100, 50), (85, 255, 255)],  # Bright green
    'Teal': [(80, 50, 50), (90, 255, 255)],   # Medium cyan
    'Turquoise': [(80, 100, 100), (100, 255, 255)],  # Bright cyan
    'Coral': [(0, 50, 100), (20, 255, 255)],  # Reddish-orange
    'Gold': [(15, 100, 100), (40, 255, 255)],  # Bright yellow-orange
    'Lavender': [(130, 50, 50), (150, 255, 255)],  # Light purple
    'Violet': [(140, 50, 50), (160, 255, 255)],   # Medium purple
    'Peach': [(0, 50, 200), (20, 255, 255)],      # Light orange
    'Mint': [(35, 50, 50), (85, 255, 255)],      # Light green
    'Navy': [(100, 50, 50), (130, 255, 255)],    # Dark blue
}

# Function to speak out detected color in a separate thread
def speak_color(color_name):
    """Speak out the detected color name using text-to-speech."""
    def speak():
        engine.say(f"{color_name} detected")
        engine.runAndWait()
    # Create and start a new thread for the speech function
    speech_thread = threading.Thread(target=speak)
    speech_thread.start()

class ColorDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Real-Time Color Detection Interface")
        
        # Video Capture object
        self.cap = cv2.VideoCapture(0)
        
        # Tkinter Variables
        self.running = False  # Indicates if video feed is running
        self.audio_feedback = True  # Indicates if audio feedback is enabled
        
        # Last detected color to avoid repetition
        self.last_detected_color = None
        
        # Create Start/Stop Button
        self.btn_start = Button(self.master, text="Start Detection", command=self.start_detection, font=("Helvetica", 12))
        self.btn_start.grid(row=0, column=0, padx=10, pady=10)

        # Create Stop Button
        self.btn_stop = Button(self.master, text="Stop Detection", command=self.stop_detection, font=("Helvetica", 12), state=DISABLED)
        self.btn_stop.grid(row=0, column=1, padx=10, pady=10)

        # Create Toggle Audio Button
        self.btn_toggle_audio = Button(self.master, text="Toggle Audio Feedback", command=self.toggle_audio, font=("Helvetica", 12))
        self.btn_toggle_audio.grid(row=0, column=2, padx=10, pady=10)

        # Create a label to show the detected color name
        self.label_detected_color = Label(self.master, text="Detected Color: None", font=("Helvetica", 16))
        self.label_detected_color.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Create a canvas to display the video feed
        self.canvas = Canvas(self.master, width=640, height=480)
        self.canvas.grid(row=2, column=0, columnspan=3)

    def start_detection(self):
        """Start the color detection and video feed."""
        self.running = True
        self.btn_start.config(state=DISABLED)
        self.btn_stop.config(state=NORMAL)
        self.detect_color()

    def stop_detection(self):
        """Stop the color detection and video feed."""
        self.running = False
        self.btn_start.config(state=NORMAL)
        self.btn_stop.config(state=DISABLED)

    def toggle_audio(self):
        """Toggle audio feedback on or off.""" 
        self.audio_feedback = not self.audio_feedback
        status = "ON" if self.audio_feedback else "OFF"
        self.btn_toggle_audio.config(text=f"Audio Feedback: {status}")

    def detect_color(self):
        """Continuously capture video frames and detect colors."""
        if not self.running:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            return

        # Get the frame dimensions and calculate the center region
        height, width, _ = frame.shape
        cx, cy = width // 2, height // 2  # Center point
        region_size = 50  # Size of the square region around the center
        top_left = (cx - region_size, cy - region_size)
        bottom_right = (cx + region_size, cy + region_size)

        # Extract the center region of interest (ROI)
        center_region = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Convert the center region from BGR to HSV color space
        hsv_center = cv2.cvtColor(center_region, cv2.COLOR_BGR2HSV)

        # Initialize a variable to store the current detected color
        detected_color = None

        # Iterate through defined color ranges to find if any color is detected
        for color_name, (lower, upper) in color_ranges.items():
            lower_bound = np.array(lower)
            upper_bound = np.array(upper)

            # Create a mask for the color in the center region
            mask = cv2.inRange(hsv_center, lower_bound, upper_bound)

            # Check if the color is detected in the center region
            if np.any(mask):
                detected_color = color_name
                break

        # If a new color is detected, provide audio feedback and update the label
        if detected_color and detected_color != self.last_detected_color:
            self.label_detected_color.config(text=f"Detected Color: {detected_color}")
            if self.audio_feedback:
                speak_color(detected_color)
            self.last_detected_color = detected_color

        # Draw a rectangle around the center region for visualization
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

        # Convert the frame to a format suitable for Tkinter
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_image = Image.fromarray(frame)
        frame_image = ImageTk.PhotoImage(image=frame_image)

        # Display the frame in the Tkinter canvas
        self.canvas.create_image(0, 0, anchor=NW, image=frame_image)
        self.canvas.image = frame_image

        # Continue capturing frames
        self.master.after(10, self.detect_color)

    def __del__(self):
        """Release the video capture object and destroy the window."""
        self.cap.release()

# Create the main window
root = Tk()
app = ColorDetectionApp(root)
root.mainloop()
