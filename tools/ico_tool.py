from PIL import Image, ImageDraw, ImageFont

# 托盘相关代码
def create_image():
    """ 创建托盘图标 """
    image = Image.new('RGB', (64, 64), (0, 0, 0))
    d = ImageDraw.Draw(image)
    # 创建一个字体对象，指定字体和大小
    try:
        font = ImageFont.truetype("arial.ttf", 64)  # 使用 Arial 字体，大小为 30
    except IOError:
        font = ImageFont.load_default()  # 如果找不到字体，使用默认字体

    # 绘制蓝色矩形
    d.rectangle((0, 0, 64, 64), fill="black")
    # 绘制较大的白色字母 "S"
    d.text((10, 15), "A", fill="white", font=font)  # Y 坐标稍微向下移动
    return image
