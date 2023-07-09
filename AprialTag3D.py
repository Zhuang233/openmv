# AprilTags3D定位例程
#
# 这个例子展示了OpenMV Cam的功能，可以检测OpenMV Cam M7/H7 上的April标签。OpenMV2 M4版本无法检测april标签。

import sensor, image, time, math

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # 如果分辨率太高，内存可能溢出
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # 必须关闭此功能，以防止图像冲刷…
sensor.set_auto_whitebal(False)  # 必须关闭此功能，以防止图像冲刷…
clock = time.clock()

# 注意！与find_qrcodes不同，find_apriltags方法不需要对镜像进行镜头校正。

#标签系列有什么区别？ 那么，例如，TAG16H5家族实际上是一个4x4的方形标签。
#所以，这意味着可以看到比6x6的TAG36H11标签更长的距离。 然而，较低的H值（H5对H11）
#意味着4x4标签的假阳性率远高于6x6标签。 所以，除非你有理由使用其他标签系列，
#否则使用默认族TAG36H11。


# AprilTags库输出标签的姿势信息。 这是x / y / z平移和x / y / z旋转。
# x / y / z旋转以弧度表示，可以转换为度数。 至于翻译单位是无量纲的，
# 你必须应用一个转换函数。

# f_x是相机的x焦距。它应该等于以mm为单位的镜头焦距除以x传感器尺寸（以mm为单位）乘以图像中的像素数。
# 以下数值适用于配备2.8毫米镜头的OV7725相机。

# f_y是相机的y焦距。它应该等于以mm为单位的镜头焦距除以y传感器尺寸（以mm为单位）乘以图像中的像素数。
# 以下数值适用于配备2.8毫米镜头的OV7725相机。

# c_x是以像素为单位的图像x中心位置
# c_x是以像素为单位的图像x中心位置

# 官方相机参数
# f_x = (2.8 / 3.984) * 160 # find_apriltags 如果没有设置，则默认为这个
# f_y = (2.8 / 2.952) * 120 # find_apriltags 如果没有设置，则默认为这个
# c_x = 160 * 0.5 # find_apriltags 如果没有设置，则默认为这个 (the image.w * 0.5)
# c_y = 120 * 0.5 # find_apriltags 如果没有设置，则默认为这个 (the image.h * 0.5)

# FD5640参数（焦距2.7mm,传感器尺寸x2.36mm y1.76mm,QQVGA 160x120）
f_x = (2.7 / 2.36) * 160 # find_apriltags 如果没有设置，则默认为这个
f_y = (2.7 / 1.76) * 120 # find_apriltags 如果没有设置，则默认为这个
c_x = 160 * 0.5 # find_apriltags 如果没有设置，则默认为这个 (the image.w * 0.5)
c_y = 120 * 0.5 # find_apriltags 如果没有设置，则默认为这个 (the image.h * 0.5)

# 比例系数k
k = 1.55

def degrees(radians):
    return (180 * radians) / math.pi

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # 默认为 TAG36H11
        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        img.draw_cross(80, 60, color = (0, 255, 0))
        print_args = (tag.x_translation()*k, tag.y_translation()*k, tag.z_translation()*k, \
            degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
        # 变换单位不详。旋转单位是度数。
        print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
    print(clock.fps())
