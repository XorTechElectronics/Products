try:
    import sys
    import keyboard
    import serial
    import argparse
    import serial.tools.list_ports
    from time import sleep

    from usb_mf_motordriver import usb_mf_motordriver
    
except ImportError:
    sys.exit("""ImportError: You are probably missing some modules. Try 'pip install pyserial'""")
    
# VID and PID for AVR DU, must match values set in MCC
DU_VID = 0x04D8
DU_PID = 0x0B15

# Function for fetching virtual com-ports based on VID and PID
def GetSerialPort(vid, pid):
    serialPort = ""
    for port in serial.tools.list_ports.comports():
        if (port.vid == vid and port.pid == pid):
            serialPort = port.device

            print("Device         :",end = " ")
            print(port.device)
            print("Name           :",end = " ")
            print(port.name)
            print("Description    :",end = " ")
            print(port.description)
            print("hwid           :",end = " ")
            print(port.hwid)                        
            print("Manufacturer   :",end = " ")
            print(port.manufacturer)            
            print("Product String :",end = " ")
            print(port.product)
            print("Serial Number  :",end = " ")
            print(port.serial_number)            
    return serialPort

def printHex(input):
    return ' '.join(f'{c:0>2X}' for c in input)

def printMenu():
    print("0 : Selects all motors")
    print("1 : Selects motor 1")
    print("2 : Selects motor 2")
    print("3 : Selects motor 3")
    print("4 : Selects motor 4")
    print("a : Direction CCW")
    print("d : Direction CW")

    print("w : Increase Speed")
    print("s : Decrease Speed")

    print("e : Changes STBY, enabling or disabling all")
    print("b : Brake")
    print("space : Stop")

    print("c : Current Status")
    print("m : Menu")

def main(serialPortNum):
    # Gets default device serial port if not given
    if "" == serialPortNum:
        serialPortNum = GetSerialPort(DU_VID, DU_PID)
    
    # Starts device serial communication if serial port exists, else throws error
    print("Opening serial communication...")
    if "" != serialPortNum:
        cdcSerial = serial.Serial(serialPortNum,115200,timeout=1)
    else:
        print("CDC Virtual Serial Port number error detected - Could not start serial communication")
        print("\t 1. Make sure both the DEBUGGER and TARGET port are connected to the computer")
        print("\t 2. Disconnect other AVR devices from the computer")
        sys.exit("Error occurred")


    printMenu()


    usb_mf_motordriver_0 = usb_mf_motordriver()

    usb_mf_motordriver_0.current_state()
    
    while True:
        update_device   = 0
        debounce        = 0

        #Enable
        if keyboard.is_pressed('e'):
            update_device = 1
            usb_mf_motordriver_0.change_stby()

        #Select Motor
        if keyboard.is_pressed('0'):
            usb_mf_motordriver_0.all_motors=1
        if keyboard.is_pressed('1'):
            usb_mf_motordriver_0.all_motors=0
            usb_mf_motordriver_0.which_motor=0
        if keyboard.is_pressed('2'):
            usb_mf_motordriver_0.all_motors=0
            usb_mf_motordriver_0.which_motor=1
        if keyboard.is_pressed('3'):
            usb_mf_motordriver_0.all_motors=0
            usb_mf_motordriver_0.which_motor=2
        if keyboard.is_pressed('4'):
            usb_mf_motordriver_0.all_motors=0
            usb_mf_motordriver_0.which_motor=3

        #Direction
        if keyboard.is_pressed('a'):
            update_device = 1
            usb_mf_motordriver_0.set_direction("CCW")
            
        if keyboard.is_pressed('d'):
            update_device = 1
            usb_mf_motordriver_0.set_direction("CW")

        if keyboard.is_pressed('b'):
            update_device = 1
            usb_mf_motordriver_0.set_direction("Brake")

        if keyboard.is_pressed(' '):
            update_device = 1
            usb_mf_motordriver_0.set_direction("Stop") 


        #Speed
        if keyboard.is_pressed('w'):
            update_device = 1
            usb_mf_motordriver_0.increase_speed()

        if keyboard.is_pressed('s'):
            update_device = 1
            usb_mf_motordriver_0.decrease_speed()
            

        #Menu
        if keyboard.is_pressed('m'):
            printMenu()
            

        #c to show current status
        if keyboard.is_pressed('c'):            
            usb_mf_motordriver_0.current_state()

        #q to quit
        if keyboard.is_pressed('q'):
            print("You pressed 'q'. Exiting loop.")
            break
        
        if ( update_device == 1 ):
            #sentData        = [3, 1, 0, 1, 255, 1, 0, 1, 0]
            sentData        = usb_mf_motordriver_0.get_cdcdata()
            sentDataSize    = len(sentData)
            cdcSerial.write(sentData)
            print("Transmitting Data:")
            print(printHex(sentData))

        sleep(0.1)
    
#    receivedData = cdcSerial.read(sentDataSize)
#    print("\nReceived Data:")
#    print(receivedData)
    
    print("Closing the serial communication.")
    cdcSerial.close





    
    
if __name__ == '__main__':
    # Generate help and use messages
    parser = argparse.ArgumentParser(
    description='USB CDC Python example script for virtual serial port communication on AVR DU',
    epilog='Example: python usb_cdc_virtual_serial_port.py',
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
    '-s','--serialPortNum', help='device communication port, defaults to finding device based on VID and PID', default="")
    args = parser.parse_args()
    
    main(args.serialPortNum)
