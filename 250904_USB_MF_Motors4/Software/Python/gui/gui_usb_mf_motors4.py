import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports

class MotorControlPanel(ttk.LabelFrame):
    def __init__(self, parent, motor_id, send_command):
        super().__init__(parent, text=f"Motor {motor_id}")
        self.motor_id = motor_id
        self.send_command = send_command
        self.speed_var = tk.IntVar()

        # Speed Slider
        ttk.Label(self, text="Speed").grid(row=0, column=0, columnspan=2, pady=5)
        speed_slider = ttk.Scale(self, from_=0, to=100, orient="horizontal",
                                 variable=self.speed_var, command=self.on_speed_change)
        speed_slider.grid(row=1, column=0, columnspan=2, padx=10, sticky="ew")

        # Direction Buttons
        ttk.Button(self, text="Forward", command=self.set_forward).grid(row=2, column=0, pady=5)
        ttk.Button(self, text="Reverse", command=self.set_reverse).grid(row=2, column=1, pady=5)

        # Stop and Brake Buttons
        ttk.Button(self, text="Stop", command=self.stop_motor).grid(row=3, column=0, pady=5)
        ttk.Button(self, text="Brake", command=self.brake_motor).grid(row=3, column=1, pady=5)

    def on_speed_change(self, val):
        speed = int(float(val))
        self.send_command(f"M{self.motor_id}:SPEED:{speed}")

    def set_forward(self):
        self.send_command(f"M{self.motor_id}:DIR:FWD")

    def set_reverse(self):
        self.send_command(f"M{self.motor_id}:DIR:REV")

    def stop_motor(self):
        self.send_command(f"M{self.motor_id}:STOP")

    def brake_motor(self):
        self.send_command(f"M{self.motor_id}:BRAKE")

class MotorControlGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("4-Motor USB CDC Control")
        self.serial_port = None

        # USB Detection
        ttk.Button(root, text="Detect USB Device", command=self.detect_usb_device).pack(pady=5)
        self.status_label = ttk.Label(root, text="Status: Not connected")
        self.status_label.pack(pady=5)

        # Motor Panels
        self.motor_frames = []
        motors_frame = ttk.Frame(root)
        motors_frame.pack(padx=10, pady=10)
        for i in range(1, 5):
            panel = MotorControlPanel(motors_frame, i, self.send_command)
            panel.grid(row=(i-1)//2, column=(i-1)%2, padx=10, pady=10, sticky="nsew")
            self.motor_frames.append(panel)

    def find_usb_cdc_device(self, keyword="USB Serial"):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if keyword.lower() in (port.description or "").lower():
                return port.device
        return None

    def detect_usb_device(self):
        device = self.find_usb_cdc_device()
        if device:
            try:
                self.serial_port = serial.Serial(device, baudrate=115200, timeout=1)
                self.status_label.config(text=f"Connected to {device}")
            except serial.SerialException as e:
                messagebox.showerror("Connection Error", f"Failed to open {device}:\n{e}")
        else:
            self.status_label.config(text="No USB CDC device found")
            messagebox.showwarning("Device Not Found", "No USB CDC device detected.")

    def send_command(self, command):
        if self.serial_port and self.serial_port.is_open:
            try:
                self.serial_port.write((command + "\n").encode())
            except serial.SerialException as e:
                messagebox.showerror("Serial Error", f"Failed to send command:\n{e}")
        else:
            messagebox.showwarning("Not Connected", "Please detect and connect to a USB CDC device first.")

    def on_close(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MotorControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()