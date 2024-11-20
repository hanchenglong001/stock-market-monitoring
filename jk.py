from tkinter import Tk, Label, Frame,Menu
from threading import Thread
from datetime import datetime

from config import init_conf
from tools.market_data_tool import get_stock_data
from tools.ico_tool import creat_ico
from tools.state_manager import State_Box
from UI.small_module.notify_box import notify_box



stocks = init_conf.get_keys("stock")
ms = init_conf.get_value("update", 'time')
State_Box.set_state("stocks", stocks)

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




    def creat_main_ui(self):
        # 创建托盘图标
        self.icon = creat_ico(self)
        Thread(target=self.icon.run, daemon=True).start()
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
        if State_Box.get_state("window_state"):
            """ 隐藏窗口并显示托盘图标 """
            self.root.withdraw()  # 隐藏窗口
            State_Box.set_state("window_state", 0)
        else:
            """ 显示窗口 """
            self.root.deiconify()
            State_Box.set_state("window_state", 1)


        if self.icon is None:  # 检查是否已经存在托盘图标
            icon = creat_ico(self)
            Thread(target=icon.run, daemon=True).start()
        else:
            self.icon.visible = True  # 如果托盘图标已存在，则使其可见



    # 更新浮窗内容
    def update_label(self):
        now = datetime.now()
        if 9 <= now.hour < 16 or len(self.stock_frame.winfo_children()) == 0:
            try:
                stock_values = get_stock_data(stocks)
                for widget in self.stock_frame.winfo_children():
                    widget.destroy()

                max_width = 0
                for stock_name, stock_v in stock_values.items():
                    hjg_value=State_Box.get_state("hjg_value")
                    ljg_value=State_Box.get_state("ljg_value")
                    yj_h_status=State_Box.get_state("yj_h_status")
                    yj_l_status=State_Box.get_state("yj_l_status")
                    if hjg_value != 0 and yj_h_status == 0:
                        if float(stock_v[0]) > float(hjg_value):
                            notify_box(self.icon, "h")
                    if ljg_value != 0 and yj_l_status == 0:
                        if float(stock_v[0]) < float(ljg_value):
                            notify_box(self.icon, "l")

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




