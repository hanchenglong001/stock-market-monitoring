from tkinter import Label, Frame, Toplevel, Entry, Button, StringVar, Radiobutton,Listbox,END, ttk
from tools.login_tool import get_a_stock

def add_stock_window(root):
    add_stock_window = Toplevel(root)
    add_stock_window.title("添加股票")
    add_stock_window.geometry("400x400")

    # 定义更新表格数据的函数
    def update_table(tree, root):
        # 检查窗口是否已销毁
        if not root.winfo_exists():
            return  # 如果窗口不存在，则退出线程
        # 清空当前表格内容
        for row in tree.get_children():
            tree.delete(row)

        # 获取新数据并填充表格
        data = get_a_stock()
        for k,v in data.items():
            tree.insert('', 'end', values=(k,v))

    def search_stock():
        query = search_entry.get()
        update_table(tree, add_stock_window, query)  # 更新表格数据，使用查询条件

    # 搜索框和按钮
    search_label = Label(add_stock_window, text="输入股票代码或名称进行搜索:")
    search_label.pack(pady=5)

    search_entry = Entry(add_stock_window)
    search_entry.pack(pady=5)

    search_button = Button(add_stock_window, text="搜索", command=search_stock)
    search_button.pack(pady=5)

    # Treeview 样式
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=15)  # 行高
    style.map("Treeview", background=[('selected', 'darkgray')])
    # 创建 Treeview 表格
    columns = ('股票名称', '股票代码')
    tree = ttk.Treeview(add_stock_window, columns=columns, show='headings', height=10)
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    # 定义表头和列宽
    tree.heading('股票名称', text='股票名称')
    tree.column('股票名称', width=100, anchor='center')
    tree.heading('股票代码', text='股票代码')
    tree.column('股票代码', width=100, anchor='center')






    # 初次填充数据
    update_table(tree, add_stock_window)

def del_stock_window(root):
    del_stock_window = Toplevel(root)
    del_stock_window.title("删除股票")
    del_stock_window.geometry("400x400")