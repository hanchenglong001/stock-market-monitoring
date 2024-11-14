from tkinter import Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton
from tools.state_manager import State_Box
from tools.market_data_tool import get_one_stock_data
from UI.model.labeled_entry import add_labeled_entry


def send_warning(root):
    def get_stock_jg():
        stock_data = get_one_stock_data(selected_stock.get())

        entry_cost.delete(0, 'end')  # 清空输入框
        entry_cost.insert(0, stock_data[1])  # 插入当前价格
        entry_current_price.delete(0, 'end')  # 清空输入框
        entry_current_price.insert(0, stock_data[0])  # 插入当前价格
        print(stock_data)
        pass

    def set_yj():
        State_Box.set_state("hjg_value", hjg.get() if hjg.get() else 0)
        State_Box.set_state("ljg_value", ljg.get() if ljg.get() else 0)
        vlaue = f"设置成功 预警上限：{State_Box.get_state('hjg_value')} 预警下限：{State_Box.get_state('ljg_value')}"
        stock_yj_info_label.config(text=vlaue)
        State_Box.set_state("yj_h_status", 0)
        State_Box.set_state("yj_l_status", 0)

    yujing_window = Toplevel(root)
    yujing_window.title("预警")
    yujing_window.geometry("400x400")

    stocks = State_Box.get_state("stocks")
    selected_stock = StringVar(value=stocks[0])
    Label(yujing_window, text="选择股票:").pack()
    for stock in stocks:
        Radiobutton(yujing_window, text=stock, variable=selected_stock, value=stock).pack(anchor='w')
    Button(yujing_window, text="获取股票数据", command=get_stock_jg).pack()

    # 将标签和输入框放在同一行


    entry_cost = add_labeled_entry(yujing_window,"成本价格:")
    entry_current_price = add_labeled_entry(yujing_window,"当前价格:")
    hjg = add_labeled_entry(yujing_window,"预警上限:")
    ljg = add_labeled_entry(yujing_window,"预警下限:")
    hjg.pack()
    ljg.pack()

    entry_cost.pack()
    entry_current_price.pack()

    Button(yujing_window, text="设置", command=set_yj).pack()
    stock_yj_info_label = Label(yujing_window, text="")
    stock_yj_info_label.pack()
