from tkinter import  Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton
from tools.state_manager import State_Box


def replenish_stock(self, icon, item):
    # 创建补仓计算窗口
    buchang_window = Toplevel(self.root)
    buchang_window.title("补仓计算")
    buchang_window.geometry("400x400")

    stocks=State_Box.get_state("stocks")
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
