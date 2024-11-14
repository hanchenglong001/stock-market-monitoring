from tkinter import Tk, Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton

from threading import Thread
from datetime import datetime
from pystray import MenuItem as item
from pystray import Icon, Menu


from tools.bucang import get_required_shares
from config import init_conf
from tools.market_data_tool import get_one_stock_data,get_stock_data
from tools.ico_tool import create_image,creat_ico
from tools.state_manager import State_Box
from UI.model.replenish import replenish_stock
from UI.model.forewarning import send_warning
from UI.model.notify_box import notify_box


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

        # 创建托盘图标
        self.icon = creat_ico(self)



    def creat_main_ui(self):
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
        """ 隐藏窗口并显示托盘图标 """
        self.root.withdraw()  # 隐藏窗口

        if self.icon is None:  # 检查是否已经存在托盘图标
            icon = creat_ico(self)
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
        State_Box.set_state("hjg_value",self.hjg.get() if self.hjg.get() else 0)
        State_Box.set_state("ljg_value",self.ljg.get() if self.ljg.get() else 0)
        vlaue = f"设置成功 预警上限：{State_Box.get_state('hjg_value')} 预警下限：{State_Box.get_state('ljg_value')}"
        self.stock_yj_info_label.config(text=vlaue)
        State_Box.set_state("yj_h_status", 0)
        State_Box.set_state("yj_l_status", 0)


    def yujing(self, icon, item):
        send_warning(self,icon, item)

    def bucang(self, icon, item):
        replenish_stock(self,icon, item)

    def on_notify(self, icon, item):
        notify_box(self,icon, item)

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
                            self.on_notify(self.icon, "h")
                    if ljg_value != 0 and yj_l_status == 0:
                        if float(stock_v[0]) < float(ljg_value):
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
