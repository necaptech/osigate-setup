s_port = '/dev/ttyS0'
b_rate = 1200

from time import sleep
import serial

ser = serial.Serial(
    port=s_port,
    baudrate=b_rate,
    timeout=2,
    write_timeout=1
)

while True:
    byteForm = bytes.fromhex("5230303032370000ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000024a0ff0")
    print(byteForm)
    print(ser.write(byteForm))
    sleep(5)

# 0FF0 to send, F00F to receive
# Need to send five times when changed, sent += 1 only when sent this, priority to older.
