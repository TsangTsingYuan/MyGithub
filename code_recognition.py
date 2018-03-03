from PIL import Image

im = Image.open('code.jpg')
#灰度处理
imgry = im.convert('L')
#imgry.show()
table = []
#二值化处理  threshold:Integer 图像二值化阀值
def twoValue(image,threshold):
    #threshold = 130
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return image.point(table, '1')


# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），
# 当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# N: Integer 降噪率 0 <N <8
# image: 灰度图
# 输出
#  0：白色
#  1：黑色
#如何去模糊
def clearNoise(image, N):
    pixdata = image.load()  # RGB数据
    print(image.getpixel((0, 0)))
    w, l = image.size   #图片大小
    for i in range(0, N):
        for x in range(0, w-i):
            for y in range(0, l-i):
                if pixdata[x+i, y] ==1:
                    if pixdata[x, y+i] ==1:
                        # 将rgb转化为像素 白色
                        image.putpixel((x, y), 1)

out = twoValue(imgry, 130)
clearNoise(out, 3)
out.show()