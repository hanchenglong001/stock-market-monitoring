from tkinter import Tk, Label, Frame, Toplevel, Entry, Button, messagebox, StringVar, Radiobutton
from requests import get
from threading import Thread
from datetime import datetime
from pystray import MenuItem as item
from pystray import Icon, Menu
from PIL import Image, ImageDraw, ImageFont
from configparser import ConfigParser
from bucang import get_required_shares


class init_config():
    def __init__(self, config_file: str):
        cfg = ConfigParser()
        cfg.read(config_file, encoding='utf-8')
        self.cfg = cfg

    def get_value(self, section, key):
        if section in self.cfg:
            return self.cfg[section][key]
        else:
            raise Exception(f"配置项不存在{section}.{key}")

    def get_keys(self, section):
        keys = []
        for i in self.cfg[section]:
            keys.append(i)
        return keys


init_conf = init_config("config.ini")
stocks = init_conf.get_keys("stock")
ms = init_conf.get_value("update", 'time')


# 获取多个股票的实时数据
def get_stock_data():
    stock_urls = {}
    stock_ben = {}
    for name in stocks:
        stockvlue = init_conf.get_value("stock", name)
        _ = stockvlue.split(";")
        stock = _[0]
        stock_ben[name] = _[1] if len(_) > 1 else 0
        stock_urls[name] = f"https://hq.sinajs.cn/list={stock}"

    headers = {"Referer": "https://finance.sina.com.cn"}
    stock_data = {}
    for stock_name, url in stock_urls.items():
        response = get(url, headers=headers)
        data = response.text.split(",")
        if len(data) > 30:
            current_index = data[3]
            yesterday_index = data[2]
            stock_data[stock_name] = [current_index, stock_ben.get(stock_name), yesterday_index]
        else:
            stock_data[stock_name] = f"{stock_name}: 无法获取数据"
    return stock_data


# 获取多个股票的实时数据
def get_one_stock_data(stock):
    stock_urls = {}
    stock_ben = {}
    for name in [stock]:
        stockvlue = init_conf.get_value("stock", name)
        _ = stockvlue.split(";")
        stock = _[0]
        stock_ben[name] = _[1] if len(_) > 1 else 0
        stock_urls[name] = f"https://hq.sinajs.cn/list={stock}"

    headers = {"Referer": "https://finance.sina.com.cn"}
    stock_data = {}
    stock_name = ''
    for stock_name, url in stock_urls.items():
        response = get(url, headers=headers)
        data = response.text.split(",")
        if len(data) > 30:
            current_index = data[3]
            yesterday_index = data[2]
            stock_data[stock_name] = [current_index, stock_ben.get(stock_name), yesterday_index]
        else:
            stock_data[stock_name] = f"{stock_name}: 无法获取数据"
    return stock_data[stock_name]


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


class jk_ui:
    def __init__(self):
        # 全局变量来存储托盘图标
        self.icon = None
        # 创建一个透明浮窗
        self.root = Tk()
        self.root.overrideredirect(True)
        self.root.geometry("+1000+100")
        self.root.configure(bg="black")
        # 创建一个Frame用于放置多个Label
        self.stock_frame = Frame(self.root, bg="black")
        self.stock_frame.pack()

        # 创建托盘图标
        self.icon = Icon("stock_tracker", create_image(), menu=Menu(
            item('预警', self.yujing),
            item('补仓', self.bucang),
            item('打开', self.show_window),
            item('最小化', self.minimize_to_tray),
            item('关闭', self.quit_window)
        ))

        self.hjg_value = 0
        self.ljg_value = 0
        self.yj_h_status = 0
        self.yj_l_status = 0

        Thread(target=self.icon.run, daemon=True).start()

    def creat_main_ui(self):
        # 绑定鼠标事件实现窗口拖动
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.on_motion)
        # 启动实时更新线程
        self.update_label()
        # 透明浮窗设置
        self.make_window_topmost_and_transparent()
        # 进入主循环
        self.root.mainloop()

    def quit_window(self, icon, item):
        """ 退出程序 """
        icon.stop()
        self.root.quit()

    def minimize_to_tray(self, event):
        """ 隐藏窗口并显示托盘图标 """
        self.root.withdraw()  # 隐藏窗口

        if self.icon is None:  # 检查是否已经存在托盘图标
            icon = Icon("stock_tracker", create_image(), menu=Menu(
                item('预警', self.yujing),
                item('补仓', self.bucang),
                item('打开', self.show_window),
                item('最小化', self.minimize_to_tray),
                item('关闭', self.quit_window)

            ))
            Thread(target=icon.run, daemon=True).start()
        else:
            self.icon.visible = True  # 如果托盘图标已存在，则使其可见

    def show_window(self, icon, item):
        """ 显示窗口 """
        self.root.deiconify()

    def get_stock_jg(self):
        stock_data = get_one_stock_data(self.selected_stock.get())

        self.entry_cost.delete(0, 'end')  # 清空输入框
        self.entry_cost.insert(0, stock_data[1])  # 插入当前价格
        self.entry_current_price.delete(0, 'end')  # 清空输入框
        self.entry_current_price.insert(0, stock_data[0])  # 插入当前价格
        print(stock_data)
        pass

    def get_bucang_rel(self):
        bucang_info = get_required_shares(self.entry_holding.get(), self.entry_cost.get(),
                                          self.entry_current_price.get(), self.entry_target_price.get())
        self.stock_bucang_info_label.config(text=bucang_info)

    def set_yj(self):
        self.hjg_value = self.hjg.get() if self.hjg.get() else 0
        self.ljg_value = self.ljg.get() if self.ljg.get() else 0
        vlaue = f"设置成功 预警上限：{self.hjg_value} 预警下限：{self.ljg_value}"
        self.stock_yj_info_label.config(text=vlaue)
        self.yj_h_status = 0
        self.yj_l_status = 0

    def yujing(self, icon, item):
        # 创建补仓计算窗口
        yujing_window = Toplevel(self.root)
        yujing_window.title("预警")
        yujing_window.geometry("400x400")

        self.selected_stock = StringVar(value=stocks[0])
        Label(yujing_window, text="选择股票:").pack()
        for stock in stocks:
            Radiobutton(yujing_window, text=stock, variable=self.selected_stock, value=stock).pack(anchor='w')
        Button(yujing_window, text="获取股票数据", command=self.get_stock_jg).pack()

        # 将标签和输入框放在同一行
        def add_labeled_entry(label_text):
            frame = Frame(yujing_window)
            frame.pack(padx=10, pady=5, fill='x')
            Label(frame, text=label_text).pack(side='left')
            entry = Entry(frame)
            entry.pack(side='left', expand=True, fill='x')
            return entry

        self.entry_cost = add_labeled_entry("成本价格:")
        self.entry_current_price = add_labeled_entry("当前价格:")
        self.hjg = add_labeled_entry("预警上限:")
        self.ljg = add_labeled_entry("预警下限:")
        self.hjg.pack()
        self.ljg.pack()

        self.entry_cost.pack()
        self.entry_current_price.pack()

        Button(yujing_window, text="设置", command=self.set_yj).pack()
        self.stock_yj_info_label = Label(yujing_window, text="")
        self.stock_yj_info_label.pack()

    def bucang(self, icon, item):
        # 创建补仓计算窗口
        buchang_window = Toplevel(self.root)
        buchang_window.title("补仓计算")
        buchang_window.geometry("400x400")

        self.selected_stock = StringVar(value=stocks[0])
        Label(buchang_window, text="选择股票:").pack()
        for stock in stocks:
            Radiobutton(buchang_window, text=stock, variable=self.selected_stock, value=stock).pack(anchor='w')
        Button(buchang_window, text="获取股票数据", command=self.get_stock_jg).pack()

        # 将标签和输入框放在同一行
        def add_labeled_entry(label_text):
            frame = Frame(buchang_window)
            frame.pack(padx=10, pady=5, fill='x')
            Label(frame, text=label_text).pack(side='left')
            entry = Entry(frame)
            entry.pack(side='left', expand=True, fill='x')
            return entry

        self.entry_cost = add_labeled_entry("成本价格:")
        self.entry_current_price = add_labeled_entry("当前价格:")
        self.entry_target_price = add_labeled_entry("目标价格:")
        self.entry_holding = add_labeled_entry("持有数量:")

        self.entry_holding.pack()
        self.entry_cost.pack()
        self.entry_current_price.pack()
        self.entry_target_price.pack()
        Button(buchang_window, text="计算", command=self.get_bucang_rel).pack()
        self.stock_bucang_info_label = Label(buchang_window, text="")
        self.stock_bucang_info_label.pack()

    # 定义点击菜单项的回调函数
    def on_notify(self, icon, item):
        if item == "h":
            icon.notify(title="预警上限", message="老板发财了")
            self.yj_h_status = 1
        if item == "l":
            icon.notify(title="预警下限", message="老板准备跑路了")
            self.yj_l_status = 1

    # 更新浮窗内容
    def update_label(self):
        now = datetime.now()
        if 9 <= now.hour < 16 or len(self.stock_frame.winfo_children()) == 0:
            try:
                stock_values = get_stock_data()
                for widget in self.stock_frame.winfo_children():
                    widget.destroy()

                max_width = 0
                for stock_name, stock_v in stock_values.items():
                    if self.hjg_value != 0 and self.yj_h_status == 0:
                        if float(stock_v[0]) > float(self.hjg_value):
                            self.on_notify(self.icon, "h")
                    if self.ljg_value != 0 and self.yj_l_status == 0:
                        if float(stock_v[0]) < float(self.ljg_value):
                            self.on_notify(self.icon, "l")

                    if float(stock_v[1]) == 0:
                        difference, differenceb = "", "*"
                    else:
                        difference = round(float(stock_v[0]) - float(stock_v[1]), 3)
                        differenceb = round((float(stock_v[0]) - float(stock_v[1])) / float(stock_v[1]) * 100, 2)
                    zf = round((float(stock_v[0]) - float(stock_v[2])) / float(stock_v[2]) * 100, 2)
                    if zf > 0:
                        fg = "red"
                    else:
                        fg = "green"
                    stock_label = Label(self.stock_frame,
                                        text=f"{stock_name}:{stock_v[0]}  {zf}%   {differenceb}%   {difference} ",
                                        fg=fg,
                                        bg="black", font=("Arial", 10))
                    stock_label.pack(anchor="w")
                    stock_label.update_idletasks()
                    max_width = max(max_width, stock_label.winfo_width())

                self.root.geometry(f"{self.root.winfo_width()}x{self.stock_frame.winfo_height() + 20}")
            except Exception as e:
                print(f"Error: {e}")
                stock_label = Label(self.stock_frame, text="获取数据失败", bg="black", font=("Arial", 18))
                stock_label.pack(anchor="w")
        self.root.after(int(ms) * 1000, self.update_label)

    def make_window_topmost_and_transparent(self):
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)
        self.root.attributes("-transparentcolor", "black")

    def start_move(self, event):
        self.root.x = event.x
        self.root.y = event.y

    def on_motion(self, event):
        x = event.x_root - self.root.x
        y = event.y_root - self.root.y
        self.root.geometry(f"+{x}+{y}")


if __name__ == '__main__':
    jk_ui = jk_ui()
    jk_ui.creat_main_ui()
