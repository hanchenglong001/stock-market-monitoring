from PIL import Image, ImageDraw, ImageFont
from pystray import MenuItem as item
from pystray import Icon, Menu
from UI.model.replenish import replenish_stock
from UI.model.forewarning import send_warning
from UI.model.nephogram import open_stock_plate
from UI.model.bk_show import show_dropdown_bk
from UI.small_module.about_software import software_info
from UI.model.set_conf import create_modify_config_window
# from UI.model.stock_add_del import show_dropdown_bk




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




def creat_ico(self):
    return Icon("stock_tracker", create_image(), menu=Menu(
        item('关于', lambda: software_info(self.root)),
        item('工具', Menu(
        item('大盘云图', open_stock_plate),
               item('预警', lambda: send_warning(self.root)),
               item('补仓', lambda: replenish_stock(self.root)),
               item('板块数据',lambda: show_dropdown_bk(self.root)),
        )),
        item( "展示/隐藏", self.minimize_to_tray),
        item( "设置",Menu(
            # item("添加/删除股票",),
            item("配置修改",lambda: create_modify_config_window(self.root))
        )),
        item('关闭', self.quit_window)
    ))