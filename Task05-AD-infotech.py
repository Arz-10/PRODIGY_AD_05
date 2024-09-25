import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import webbrowser
import pyperclip

# Colors
eggshell = "#F0EAD6"
turquoise_blue = "#00CED1"
black = "#000000"
magenta = "#FF00FF"

# Global variable for the camera
cap = None
is_scanning = False  # Flag to control scanning state

# QR Code scanning function using cv2.QRCodeDetector
def scan_qr_code():
    global cap, is_scanning
    if not is_scanning:
        return  # If scanning is stopped, do nothing

    if cap is None:
        cap = cv2.VideoCapture(0)  # Open the camera

    detector = cv2.QRCodeDetector()  # Initialize the QRCodeDetector
    ret, frame = cap.read()  # Read frame from the camera
    if not ret:
        messagebox.showerror("Error", "Failed to open the camera.")
        return

    # Detect and decode the QR code
    data, bbox, _ = detector.detectAndDecode(frame)

    # If data is detected, show it
    if data:
        result.set(data)
        release_camera()
        return

    # Display the camera feed in the app
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=img)
    camera_frame.imgtk = imgtk
    camera_frame.configure(image=imgtk)

    # Continue scanning after a delay
    camera_frame.after(10, scan_qr_code)

# Function to start scanning
def start_scanning():
    global is_scanning
    if not is_scanning:  # Prevent restarting if already scanning
        result.set("")  # Clear the previous result
        is_scanning = True
        scan_qr_code()  # Start the scanning process
        scan_button.config(state=tk.DISABLED)
        stop_button.config(state=tk.NORMAL)

# Function to stop scanning
def stop_scanning():
    global is_scanning
    if is_scanning:
        is_scanning = False  # Stop the scanning loop
        release_camera()  # Release the camera
        scan_button.config(state=tk.NORMAL)
        stop_button.config(state=tk.DISABLED)

# Function to release the camera
def release_camera():
    global cap
    if cap is not None:
        cap.release()  # Stop the camera
        cv2.destroyAllWindows()
        cap = None

# Copy the scanned QR code data
def copy_data():
    data = result.get()
    if data:
        pyperclip.copy(data)
        messagebox.showinfo("Copied", "Data copied to clipboard!")
    else:
        messagebox.showwarning("No Data", "No QR code data available to copy.")

# Open the link in a browser
def open_link():
    url = result.get()
    if url:
        webbrowser.open(url)
    else:
        messagebox.showwarning("No Data", "No QR code data available to open.")

# Create the main window
app = tk.Tk()
app.title("QR Code Scanner")
app.geometry("600x600")
app.configure(bg=turquoise_blue)

# Camera feed display area
camera_frame = ttk.Label(app)
camera_frame.pack(pady=10)

# Label for displaying the scanned QR code data
result = tk.StringVar()
result_label = ttk.Label(app, textvariable=result, font=("Helvetica", 14), background=turquoise_blue, foreground=black)
result_label.pack(pady=10)

# Button styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TButton", background=eggshell, foreground=black)

# Start scanning button
scan_button = ttk.Button(app, text="Start Scanning", command=start_scanning, style="TButton")
scan_button.pack(pady=10)

# Stop scanning button
stop_button = ttk.Button(app, text="Stop Scanning", command=stop_scanning, style="TButton")
stop_button.pack(pady=10)
stop_button.config(state=tk.DISABLED)  # Initially disabled

button_frame = tk.Frame(app, bg=turquoise_blue)
button_frame.pack(pady=10)

copy_button = ttk.Button(button_frame, text="Copy Data", command=copy_data, style="TButton")
copy_button.grid(row=0, column=0, padx=10)

open_button = ttk.Button(button_frame, text="Open Link", command=open_link, style="TButton")
open_button.grid(row=0, column=1, padx=10)

app.option_add("*TButton*background", eggshell)
app.option_add("*TButton*foreground", black)

app.mainloop()