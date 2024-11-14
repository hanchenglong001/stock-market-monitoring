from tkinter import  Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton
from tools.state_manager import State_Box
from tools.market_data_tool import get_one_stock_data
from tools.bucang import get_required_shares
from UI.model.labeled_entry import add_labeled_entry


def replenish_stock(root):
    def get_stock_jg():
        stock_data = get_one_stock_data(selected_stock.get())

        entry_cost.delete(0, 'end')  # 清空输入框
        entry_cost.insert(0, stock_data[1])  # 插入当前价格
        entry_current_price.delete(0, 'end')  # 清空输入框
        entry_current_price.insert(0, stock_data[0])  # 插入当前价格
        print(stock_data)
        pass

    def get_bucang_rel():
        bucang_info = get_required_shares(entry_holding.get(), entry_cost.get(),
                                          entry_current_price.get(), entry_target_price.get())
        stock_bucang_info_label.config(text=bucang_info)


    # 创建补仓计算窗口
    buchang_window = Toplevel(root)
    buchang_window.title("补仓计算")
    buchang_window.geometry("400x400")

    stocks=State_Box.get_state("stocks")
    selected_stock = StringVar(value=stocks[0])
    Label(buchang_window, text="选择股票:").pack()
    for stock in stocks:
        Radiobutton(buchang_window, text=stock, variable=selected_stock, value=stock).pack(anchor='w')
    Button(buchang_window, text="获取股票数据", command=get_stock_jg).pack()




    entry_cost = add_labeled_entry(buchang_window,"成本价格:")
    entry_current_price = add_labeled_entry(buchang_window,"当前价格:")
    entry_target_price = add_labeled_entry(buchang_window,"目标价格:")
    entry_holding = add_labeled_entry(buchang_window,"持有数量:")

    entry_holding.pack()
    entry_cost.pack()
    entry_current_price.pack()
    entry_target_price.pack()
    Button(buchang_window, text="计算", command=get_bucang_rel).pack()
    stock_bucang_info_label = Label(buchang_window, text="")
    stock_bucang_info_label.pack()
