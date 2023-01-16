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

for index in range(3):
    byteForm = bytes.fromhex("5230303032370000ff0001000000000000000000000000000000000000000000024b0ff0")
    print(byteForm)
    print(ser.write(byteForm))
    sleep(3)

# 0FF0 to send, F00F to receive
# Need to send five times when changed, sent += 1 only when sent this, priority to older.
