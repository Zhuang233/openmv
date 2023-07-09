import struct,time
from pyb import UART

uart3 = UART(3,9600)

def float_to_bytes(f):
    # 将浮点数转换为字节数组
    b = struct.pack('!f', f)
    return bytearray(b)

f = 1.234
byte_array = float_to_bytes(f)

while True:
    uart3.write(byte_array)
    time.sleep_ms(1000)
