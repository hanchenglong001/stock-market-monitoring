from tkinter import Label, Frame, Toplevel, Entry, ttk,Button

from UI.small_module.labeled_entry import add_labeled_entry
from tools.login_tool import get_a_stock,add_stock,del_stock,get_stock_info
from tools.state_manager import State_Box

def show_del_message(root,message):
    # 获取父窗口的坐标
    window_x = root.winfo_rootx()
    window_y = root.winfo_rooty()

    # 获取父窗口的宽高
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # 自定义消息框的位置
    popup_x = window_x + window_width // 2 - 100  # 弹窗在父窗口中居中
    popup_y = window_y + window_height // 2 - 50

    # 创建Toplevel窗口作为自定义消息框
    message_window = Toplevel(root)
    message_window.title("")
    message_window.geometry(f"200x100+{popup_x}+{popup_y}")  # 设置大小和位置
    Label(message_window, text=message, padx=10, pady=10).pack()


# 设置弹出窗口位置
def show_add_message(root, stock_name, stock_code):
    # 获取父窗口的坐标
    window_x = root.winfo_rootx()
    window_y = root.winfo_rooty()

    # 获取父窗口的宽高
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # 自定义消息框的位置
    popup_x = window_x + window_width // 2 - 100  # 弹窗在父窗口中居中
    popup_y = window_y + window_height // 2 - 50

    # 创建Toplevel窗口作为自定义消息框
    message_window = Toplevel(root)
    message_window.title("")
    message_window.geometry(f"200x100+{popup_x}+{popup_y}")  # 设置大小和位置

    entry_cost = add_labeled_entry(message_window,"成本价格:")
    entry_cost.pack()
    def req_add_stock_api():
        response_code,rel=add_stock(stock_code, stock_name, entry_cost.get() if entry_cost.get() else "0")
        if response_code:
            Label(message_window, text=f"已将 {stock_name} 添加到自选股", padx=10, pady=10).pack()
            get_stock_info()
        else:
            Label(message_window, text=rel.get("message"), padx=10, pady=10).pack()
    Button(message_window, text="添加", command=req_add_stock_api).pack()



def add_stock_window(root):
    add_stock_windowc = Toplevel(root)
    add_stock_windowc.title("添加股票")
    add_stock_windowc.geometry("400x400")


    batch_size = 50  # 每次加载的数据条数
    current_index = 0  # 当前已加载数据的起始索引


    # 定义更新表格数据的函数
    def update_table(tree_cli, root_cli, query=None,clear=False):
        nonlocal current_index
        # 检查窗口是否已销毁
        if not root_cli.winfo_exists():
            return  # 如果窗口不存在，则退出线程
        # # 清空当前表格内容
        if clear:
            for row in tree_cli.get_children():
                tree_cli.delete(row)
        # 获取新数据并填充表格
        data = State_Box.get_state("A_stocks")
        if not data:
            State_Box.set_state("A_stocks", get_a_stock())
            data = State_Box.get_state("A_stocks")

        # 计算显示的数据范围
        start_index = current_index
        end_index = start_index + batch_size
        data_slice = list(data.items())[start_index:end_index]

        if query:
            new_data={}
            for k,v in data.items():
                if (query in k) or (query in v):
                        new_data[k]=v
            data_slice=list(new_data.items())[start_index:end_index]

        for k,v in data_slice:
            tree_cli.insert('', 'end', values=(k, v))


    def search_stock(event):
        nonlocal current_index
        query = search_entry.get()
        current_index = 0
        update_table(tree, add_stock_windowc, query, clear=True)  # 更新表格数据，使用查询条件

    # 监听滚动事件，加载更多数据
    def on_scroll(*args):
        nonlocal current_index
        # 获取 Treeview 当前的垂直滚动位置
        if tree.yview()[1] == 0.8:  # 如果已经滚动到最底部
            current_index += batch_size  # 增加加载数据的起始位置
            query = search_entry.get()
            if query:
                update_table(tree, add_stock_windowc, query)  # 加载更多数据
                return
            update_table(tree, add_stock_windowc)  # 加载更多数据


    button_frame = Frame(add_stock_windowc)
    button_frame.pack(pady=5)  # 使按钮居中并填充

    # 搜索框和按钮
    search_label = Label(button_frame, text="输入股票代码名称搜索:")
    search_label.pack(side="left", padx=5)
    search_entry = Entry(button_frame)
    search_entry.pack(side="left", padx=5)


    # 绑定输入事件，当用户输入时自动搜索
    search_entry.bind("<KeyRelease>", search_stock)

    # Treeview 样式
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=15)  # 行高
    style.map("Treeview", background=[('selected', 'darkgray')])
    # 创建 Treeview 表格
    columns = ('股票代码', '股票名称')
    tree = ttk.Treeview(add_stock_windowc, columns=columns, show='headings', height=10)
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    # 定义表头和列宽
    tree.heading('股票名称', text='股票名称')
    tree.column('股票名称', width=100, anchor='center')
    tree.heading('股票代码', text='股票代码')
    tree.column('股票代码', width=100, anchor='center')


    # 创建垂直滚动条并与 Treeview 绑定
    yscroll = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side='right', fill='y')
    # 绑定滚动事件

    tree.bind('<MouseWheel>', on_scroll)  # 鼠标滚轮触发
    tree.bind("<Down>", on_scroll)
    # 双击左键添加自选股
    def add_stocks(event):
        selected_item = tree.selection()
        if selected_item:
            stock_code, stock_name = tree.item(selected_item, 'values')
            show_add_message(tree, stock_name, stock_code)


    tree.bind("<Double-1>", add_stocks)  # 左键双击添加自选股

    # 初次填充数据
    update_table(tree, add_stock_windowc)



def del_stock_window(root):
    del_stock_windowc = Toplevel(root)
    del_stock_windowc.title("删除股票")
    del_stock_windowc.geometry("400x400")

    # 定义更新表格数据的函数
    def update_table(tree_cli, root_cli):
        # 检查窗口是否已销毁
        if not root_cli.winfo_exists():
            return  # 如果窗口不存在，则退出线程
        # # 清空当前表格内容
        for row in tree_cli.get_children():
            tree_cli.delete(row)

        data = State_Box.get_state("stocks")

        for k in data:
            tree_cli.insert('', 'end', values=(k.get("code"), k.get("name")))

    # 监听滚动事件，加载更多数据
    def on_scroll(*args):
        # 获取 Treeview 当前的垂直滚动位置
        if tree.yview()[1] == 0.8:  # 如果已经滚动到最底部
            update_table(tree, del_stock_windowc)  # 加载更多数据



    # Treeview 样式
    style = ttk.Style()
    style.configure("Treeview",
                    rowheight=15)  # 行高
    style.map("Treeview", background=[('selected', 'darkgray')])
    # 创建 Treeview 表格
    columns = ('股票代码', '股票名称')
    tree = ttk.Treeview(del_stock_windowc, columns=columns, show='headings', height=10)
    tree.pack(fill='both', expand=True, padx=10, pady=10)
    # 定义表头和列宽
    tree.heading('股票名称', text='股票名称')
    tree.column('股票名称', width=100, anchor='center')
    tree.heading('股票代码', text='股票代码')
    tree.column('股票代码', width=100, anchor='center')


    # 创建垂直滚动条并与 Treeview 绑定
    yscroll = ttk.Scrollbar(tree, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side='right', fill='y')
    # 绑定滚动事件

    tree.bind('<MouseWheel>', on_scroll)  # 鼠标滚轮触发
    tree.bind("<Down>", on_scroll)
    # 双击左键添加自选股
    def del_stocks(event):
        selected_item = tree.selection()
        if selected_item:
            stock_code, stock_name = tree.item(selected_item, 'values')
            response_code,rel=del_stock(stock_code)
            stock_list=State_Box.get_state("stocks")
            for index,stock in enumerate(stock_list):
                if stock_code==stock.get("code"):
                    del stock_list[index]
            State_Box.set_state("stocks",stock_list)
            show_del_message(tree,rel.get("message"))
            update_table(tree, del_stock_windowc)


    tree.bind("<Double-1>", del_stocks)  # 左键双击添加自选股

    # 初次填充数据
    update_table(tree, del_stock_windowc)