from tkinter import  Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton
from tools.state_manager import State_Box


def send_warning(self, icon, item):
    # 创建补仓计算窗口
    yujing_window = Toplevel(self.root)
    yujing_window.title("预警")
    yujing_window.geometry("400x400")

    stocks=State_Box.get_state("stocks")
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