import tkinter as tk
import serial
import serial.tools.list_ports


def printHex(input):
    return ' '.join(f'{c:0>2X}' for c in input)

class MotorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Motor Control")
        self.serial_port = None

        # COM port selector
        self.port_var = tk.StringVar()
        ports = [p.device for p in serial.tools.list_ports.comports()]
        self.port_menu = tk.OptionMenu(root, self.port_var, *ports)
        self.port_menu.pack()

        # Connect button
        self.connect_btn = tk.Button(root, text="Connect", command=self.connect_serial)
        self.connect_btn.pack()

        # Motor sliders
        self.speed_slider0 = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Speed_0")
        self.speed_slider0.pack()

        self.speed_slider1 = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Speed_1")
        self.speed_slider1.pack()

        self.speed_slider2 = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Speed_2")
        self.speed_slider2.pack()
        
        self.speed_slider3 = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="Speed_3")
        self.speed_slider3.pack()

        # Direction buttons
        self.forward_btn   = tk.Button(root, text="Forward", command=lambda: self.send_command("F"))
        self.reverse_btn   = tk.Button(root, text="Reverse", command=lambda: self.send_command("R"))
        self.stop_btn      = tk.Button(root, text="Stop", command=lambda: self.send_command("S"))
        self.forward_btn.pack()
        self.reverse_btn.pack()
        self.stop_btn.pack()
            
        self.btn_0_ccw   = tk.Button(root, text="CCW",   command=self.set_ccw(0)   )
        self.btn_0_cw    = tk.Button(root, text="CW",    command=self.set_cw(0)    )
        self.btn_0_brake = tk.Button(root, text="Brake", command=self.set_brake(0) )
        self.btn_0_stop  = tk.Button(root, text="Stop",  command=self.set_stop(0)  )
        self.btn_0_ccw.pack()
        self.btn_0_cw.pack()
        self.btn_0_brake.pack()
        self.btn_0_stop.pack()
        
          
    def set_ccw(self, motor):
        #self.motor_state.set("Forward")
        self.send_command("F")

    def set_cw(self, motor):
        #self.motor_state.set("Reverse")
        self.send_command("R")

    def set_brake(self, motor):
        #self.motor_state.set("Stopped")
        self.send_command("S")

    def set_stop(self, motor):
        #self.motor_state.set("Stopped")
        self.send_command("S")

        


    def connect_serial(self):
        try:
            self.serial_port = serial.Serial(self.port_var.get(), 115200, timeout=1)
        except Exception as e:
            print("Connection failed:", e)
            
    def printHex(input):
        return ' '.join(f'{c:0>2X}' for c in input)            

    def send_command(self, cmd):
        if self.serial_port and self.serial_port.is_open:
            speed0 = self.speed_slider0.get()
            speed1 = self.speed_slider1.get()
            speed2 = self.speed_slider2.get()
            speed3 = self.speed_slider3.get()
            
            
            
            #packet = f"{cmd}:{speed}\n"
            #self.serial_port.write(packet.encode())

            
            sentData        = [3, 1, 0, 1, 255, 1, 0, 1, 0]
            
            sentData[2]     = speed;
            sentData[4]     = speed1;
            sentData[6]     = speed2;
            sentData[8]     = speed3;
                       
            self.serial_port.write(sentData)
            print("Transmitting Data:")
            print(printHex(sentData))            

root = tk.Tk()
app = MotorGUI(root)
root.mainloop()
