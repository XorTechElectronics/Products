import serial
import time

from usb_mf_motordriver import usb_mf_motordriver

# Replace with your actual device path
DEVICE_PATH = '/dev/ttyACM0'  # or '/dev/ttyUSB0'
BAUD_RATE = 115200            # Match the baud rate of your CDC device

# VID and PID for AVR DU, must match values set in MCC
DU_VID = 0x04D8
DU_PID = 0x0B15



def printHex(input):
    return ' '.join(f'{c:0>2X}' for c in input)

try:
    # Open serial connection
    cdcSerial = serial.Serial(DEVICE_PATH, BAUD_RATE, timeout=1)
    print(f"Connected to {DEVICE_PATH} at {BAUD_RATE} baud.")
    
    usb_mf_motordriver_0 = usb_mf_motordriver()

    usb_mf_motordriver_0.current_state()    
    
    
    while True:
        update_device   = 1    
    
    
    
    
    
        if ( update_device == 1 ):
            sentData        = [3, 1, 0, 1, 255, 1, 0, 1, 0]
            #sentData        = usb_mf_motordriver_0.get_cdcdata()
            sentDataSize    = len(sentData)
            cdcSerial.write(sentData)
            print("Transmitting Data:")
            print(printHex(sentData))

        time.sleep(0.1)    
    
    
    
    
    

#    # Send a command to the CDC device
#    ser.write(b'HELLO DEVICE\n')
#    print("Sent: HELLO DEVICE")
#
#    # Wait for a response
#    time.sleep(0.5)
#    response = ser.readline().decode('utf-8').strip()
#    print(f"Received: {response}")

except serial.SerialException as e:
    print(f"Serial error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
