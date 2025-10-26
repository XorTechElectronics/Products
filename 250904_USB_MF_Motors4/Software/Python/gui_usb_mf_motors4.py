import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports

def printHex(input):
    return ' '.join(f'{c:0>2X}' for c in input)

class MotorControlPanel(ttk.LabelFrame):
    def __init__(self, parent, motor_id, send_command):
        super().__init__(parent, text=f"Motor {motor_id}")
        self.motor_id = motor_id
        self.send_command = send_command
        self.speed_var = tk.IntVar()

        self.motor_in1 = 0;
        self.motor_in2 = 0;
        self.motor_pwm = 0;

        # Speed Slider
        ttk.Label(self, text="Speed").grid(row=0, column=0, columnspan=2, pady=5)
        speed_slider = ttk.Scale(self, from_=0, to=100, orient="horizontal",
                                 variable=self.speed_var, command=self.on_speed_change)
        speed_slider.grid(row=1, column=0, columnspan=2, padx=10, sticky="ew")

        # Direction Buttons
        self.btn_ccw = ttk.Button(self, text="CCW", style="Dir.TButton", command=self.set_CCW) 
        self.btn_ccw.grid(row=2, column=0, pady=5, sticky="ew")
        
        self.btn_cw  = ttk.Button(self, text="CW",  style="Dir.TButton", command=self.set_CW)
        self.btn_cw.grid(row=2, column=1, pady=5, sticky="ew")

        # Stop and Brake Buttons
        self.btn_stop = ttk.Button(self, text="Stop",  style="Stop.TButton", command=self.stop_motor) 
        self.btn_stop.grid(row=3, column=0, pady=5)
        
        self.btn_brake = ttk.Button(self, text="Brake", style="Brake.TButton", command=self.brake_motor) 
        self.btn_brake.grid(row=3, column=1, pady=5)

    def on_speed_change(self, val):
        self.motor_pwm  = int(float(val))
        self.send_command()
        
    def reset_direction_styles(self):
        self.btn_cw.configure(style="Dir.TButton")
        self.btn_ccw.configure(style="Dir.TButton")
        self.btn_stop.configure(style="Stop.TButton")
        self.btn_brake.configure(style="Brake.TButton")        

    def set_CCW(self):
        self.motor_in1 = 0;
        self.motor_in2 = 1;   
        self.reset_direction_styles()
        self.btn_ccw.configure(style="ActiveDir.TButton")        
        self.send_command()

    def set_CW(self):
        self.motor_in1 = 1;
        self.motor_in2 = 0;
        self.reset_direction_styles()
        self.btn_cw.configure (style="ActiveDir.TButton") 
        self.send_command()

    def stop_motor(self):
        self.motor_in1 = 0;
        self.motor_in2 = 0;
        self.reset_direction_styles()
        self.btn_stop.configure(style="ActiveStop.TButton")
        self.send_command()

    def brake_motor(self):
        self.motor_in1 = 1;
        self.motor_in2 = 1;        
        self.reset_direction_styles()
        self.btn_brake.configure(style="ActiveBrake.TButton")
        self.send_command()

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

    def send_command(self):

        cdcdata = [3, 0, 0, 0, 0, 0, 0, 0, 0]
        #Byte 0 : [1]   enable motors 2 and 3
        #         [0]   enable motors 0 and 1

        #Byte 1 : [1]   M0 IN 2
        #         [0]   M0 IN 1
        
        #Byte 2 : [7:0] M0 PWM

        ##repeats
        
        for panel in self.motor_frames:
            motor_id  = panel.motor_id
            motor_in1 = panel.motor_in1
            motor_in2 = panel.motor_in2
            speed     = panel.motor_pwm 

            #print("Motor : ",end="")
            #print(motor_id)
            #print("IN1 : ",end="")
            #print(motor_in1)
            #print("IN2 : ",end="")
            #print(motor_in2)            
            #print("Speed : ",end="")
            #print(speed)

            if ( motor_in1==1 ):
                cdcdata[(motor_id*2)-1]          = cdcdata[(motor_id*2)-1] + 1;
            if ( motor_in2==1 ):
                cdcdata[(motor_id*2)-1]          = cdcdata[(motor_id*2)-1] + 2;                

            cdcdata[motor_id*2]            = speed


        print(printHex(cdcdata))
        
        if self.serial_port and self.serial_port.is_open:
            try:
                #self.serial_port.write((command + "\n").encode())
                self.serial_port.write( cdcdata )
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
    style = ttk.Style(root)
    style.theme_use("clam")   # important: clam respects background/foreground

    # Neutral styles
    style.configure("Dir.TButton",   background="SystemButtonFace")
    style.configure("Stop.TButton",  background="SystemButtonFace")
    style.configure("Brake.TButton", background="SystemButtonFace")

    # Active styles
    style.configure("ActiveDir.TButton",   background="green",  foreground="white")
    style.configure("ActiveStop.TButton",  background="red",    foreground="white")
    style.configure("ActiveBrake.TButton", background="orange", foreground="black")

    # Some platforms (esp. macOS) need map() to enforce colors
    style.map("ActiveDir.TButton",   background=[("!disabled", "green")],  foreground=[("!disabled", "white")])
    style.map("ActiveStop.TButton",  background=[("!disabled", "red")],    foreground=[("!disabled", "white")])
    style.map("ActiveBrake.TButton", background=[("!disabled", "orange")], foreground=[("!disabled", "black")])

    
    app = MotorControlGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
