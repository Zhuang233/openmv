# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time
from pyb import UART

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

uart3 = UART(3,9600)

while(True):
    # clock.tick()                    # Update the FPS clock.
    # img = sensor.snapshot()         # Take a picture and return the image.
    data = bytearray([0xb3,0xb3,0x55,0x66,0x5b])
    uart3.write(data)   # 串口发送数据
    time.sleep_ms(1000)
    # print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
