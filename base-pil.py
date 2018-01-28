from PIL import Image
from PIL import ImageFilter     #图像滤波
from PIL import ImageEnhance    #图像增强
from PIL import ImageSequence   #图像序列
from PIL import PSDraw          #打印
import os, sys

#读取图像
#im = Image.open("gakki2.bmp")
with open("gakki2.bmp", "rb") as fp:
    im = Image.open(fp)
    im.show()
#图像的格式 像素大小（长宽）
# 模式（L:灰度 RGB:真彩 CMYK:印刷色彩）
#print(im.format, im.size, im.mode)
#im.show()

#sys.argv就是将程序本身和给程序参数返回一个list,
# 这个list中的索引为0的就是程序本身.因此里面的给sys.argv的参数就是list索引.
#例：在CMD中输入  python captcha-pil.py  a  b c d
# 若程序中是sys.argv[0]则输出captcha-pil.py，若程序中是sys.argv[1:]则输出[a,b,c,d]

#转换成jpg格式
'''
for infile in sys.argv[1:]:
    #分离文件名与扩展名
    f, e = os.path.splitext(infile)
    outfile = f + ".jpg"
    if infile != outfile:
        try:
            Image.open(infile).save(outfile)
        except IOError:
            print("cannot convert", infile)
'''

#缩略图
'''
size = (128, 128)

for infile in sys.argv[1:]:
    outfile = os.path.splitext(infile)[0] + ".thumbnail"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size)
            im.save(outfile, "JPEG")    #指定格式
        except IOError:
            print("cannot create thumbnail for", infile)
'''
#识别图像文件信息
'''
for infile in sys.argv[1:]:
    try:
        with Image.open(infile) as im:
            print(infile, im.format, "%dx%d" % im.size, im.mode)
    except IOError:
        pass
'''
'''
#平移图像
def roll(image, delta):
    """Roll an image sideways."""
    xsize, ysize = image.size
    delta = delta % xsize
    if delta == 0: return image

    part1 = image.crop((0, 0, delta, ysize))
    part2 = image.crop((delta, 0, xsize, ysize))
    part1.load()
    part2.load()
    #粘贴方法也可以使用透明掩码作为可选参数 模式为RGBA的图片
    image.paste(part2, (0, 0, xsize-delta, ysize))
    image.paste(part1, (xsize-delta, 0, xsize, ysize))

    return image
roll(im, 600).show()    #显示平移后图像
'''
#分割成RGB三个通道
'''
r, g, b = im.split()
print(r, g, b)
im = Image.merge("RGB", (b, g, r))
#im.show()
'''

'''
#几何变换
out = im.resize((128, 128)) #大小调整
out = im.rotate(75) # 角度旋转

#out = im.transpose(Image.FLIP_LEFT_RIGHT)   #左右翻转
#out = im.transpose(Image.FLIP_TOP_BOTTOM)  #上下翻转
#out = im.transpose(Image.ROTATE_90)
#out = im.transpose(Image.ROTATE_180)
#out = im.transpose(Image.ROTATE_270)

'''

#out = im.convert('L')   #模式转换（以RGB过渡）   转换为灰度图

#ImageFilter.BLUR为模糊滤波  ImageFilter.CONTOUR为轮廓滤波
# ImageFilter.DETAIL为细节增强滤波 ImageFilter.EDGE_ENHANCE为边缘增强滤波
#ImageFilter.EDGE_ENHANCE_MORE为深度边缘增强滤波 ImageFilter.EMBOSS为浮雕滤波
#ImageFilter.FIND_EDGES为寻找边缘信息的滤波   ImageFilter.SMOOTH为平滑滤波
#ImageFilter.SMOOTH_MORE为深度平滑滤波 ImageFilter.SHARPEN为锐化滤波

#out = im.filter(ImageFilter.SHARPEN and ImageFilter.EDGE_ENHANCE)

# multiply each pixel by 1.2
#out = im.point(lambda i: i * 1.2)   #对比度
#out.show()
'''
#处理单通道
# split the image into individual bands
source = im.split()

R, G, B = 0, 1, 2

# select regions where red is less than 100
mask = source[B].point(lambda i: i < 100 and 255)

# process the green band
out = source[G].point(lambda i: i * 0.7)

# paste the processed band back, but only where red was < 100
source[G].paste(out, None, mask)

# build a new multiband image
im = Image.merge(im.mode, source)
im.show()
'''
#ImageEnhance.Color颜色增强 ImageEnhance.Brightness亮度增强
#ImageEnhance.Sharpness锐度增强
#enh = ImageEnhance.Contrast(im) #对比度增强
#enh.enhance(1.3).show("30% more contrast")  #enhance(arg) arg:浮点数赋值


###图像序列（如GIF）
'''
im2 = Image.open("gakki.gif")
im2.seek(1) # skip to the second frame

try:
    while 1:
        im2.seek(im2.tell()+1)
        # do something to im
except EOFError:
    pass # end of sequence

for frame in ImageSequence.Iterator(im2):
    #print(frame)
    frame.show()    #一帧一帧显示
'''
'''
#不需要
title = "hopper"
box = (1*72, 2*72, 7*72, 10*72) # in points

ps = PSDraw.PSDraw() # default is sys.stdout
ps.begin_document(title)

# draw the image (75 dpi)
ps.image(box, im, 75)
ps.rectangle(box)

# draw title
ps.setfont("HelveticaNarrow-Bold", 36)
ps.text((3*72, 4*72), title)

ps.end_document()
'''


