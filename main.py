import sensor, image, time, math
#from pyb import UART

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)  # 如果分辨率太高，内存可能会溢出
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_auto_gain(False)         # 必须关闭自动增益，以防止图像冲洗
sensor.set_auto_whitebal(False)     # 必须关闭自动白平衡，以防止图像冲洗
clock = time.clock()                # 定时器对象

#uart3 = UART(3,9600)
tag_families = 0
tag_families |= image.TAG36H11      # 设置标签族

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.

    # 串口发送字节流
    #data = bytearray([0xff,0xff,0xff,0xff,0x00])
    #uart3.write(data)

    # 串口接收字节流
    #ret = uart3.read()
    #print(ret)

    for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        #print_args = (tag.id(), (180 * tag.rotation()) / math.pi)
        #print("Tag ID %d, rotation %f (degrees)" % print_args)
        print(tag.x_translation())  # tag相对镜头x位置
    #print(clock.fps())
