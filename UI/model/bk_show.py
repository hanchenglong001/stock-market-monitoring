import tkinter as tk
from tkinter import Label, Frame, Toplevel, ttk
from tools.market_bk_data import get_bk_info
from threading import Timer
from tools.state_manager import State_Box

# 定义更新表格数据的函数
def update_table(tree,root):
    # 检查窗口是否已销毁
    if not root.winfo_exists():
        return  # 如果窗口不存在，则退出线程
    # 清空当前表格内容
    for row in tree.get_children():
        tree.delete(row)

    # 获取新数据并填充表格
    data = get_bk_info()
    for item in data:
        tree.insert('', 'end', values=(
            item['行业名称'], item['最新价'], item['涨跌幅（百分比）'], item['成交量（手）'], item['成交额（元）']))

    # 定时刷新，每30秒更新一次
    bkms=int(State_Box.get_state("bkms"))
    Timer(bkms, update_table, [tree,root]).start()


def show_dropdown_bk(root):
    bk_window = Toplevel(root)
    bk_window.title("板块信息")
    bk_window.geometry("500x200")

    # Treeview 样式
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=15)  # 行高
    style.map("Treeview", background=[('selected', 'darkgray')])

    # 创建 Treeview 表格
    columns = ('行业名称', '最新价', '涨跌幅（百分比）', '成交量（手）', '成交额（元）')
    tree = ttk.Treeview(bk_window, columns=columns, show='headings', height=10)
    tree.pack(fill='both', expand=True, padx=10, pady=10)

    # 定义表头和列宽
    tree.heading('行业名称', text='行业名称')
    tree.column('行业名称', width=100, anchor='center')
    tree.heading('最新价', text='最新价')
    tree.column('最新价', width=100, anchor='center')
    tree.heading('涨跌幅（百分比）', text='涨跌幅（百分比）')
    tree.column('涨跌幅（百分比）', width=100, anchor='center')
    tree.heading('成交量（手）', text='成交量（手）')
    tree.column('成交量（手）', width=100, anchor='center')
    tree.heading('成交额（元）', text='成交额（元）')
    tree.column('成交额（元）', width=100, anchor='center')

   # 初次填充数据
    update_table(tree,bk_window)