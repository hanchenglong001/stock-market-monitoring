import tkinter as tk
from tkinter import Label, Frame, Toplevel,Menu,Toplevel,Entry,Button,messagebox
from bottle import response
from tools.login_tool import get_user_info,create_user_info,get_stock_info
from tools.state_manager import State_Box

def create_login_window(root_jk):
    root=root_jk.root
    # 创建登录窗口
    login_window = Toplevel(root)
    login_window.title("登录")
    login_window.geometry("300x200")
    # 获取屏幕的宽度和高度
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 设置登录窗口的大小
    window_width = 300
    window_height = 200

    # 计算窗口应该出现的位置
    position_top = int(screen_height / 2 - window_height / 2)
    position_left = int(screen_width / 2 - window_width / 2)

    # 设置登录窗口位置
    login_window.geometry(f"{window_width}x{window_height}+{position_left}+{position_top}")

    # 用户名和密码输入框
    Label(login_window, text="用户名:").pack(pady=5)
    username_entry = Entry(login_window)
    username_entry.pack(pady=5)

    Label(login_window, text="密码:").pack(pady=5)
    password_entry = Entry(login_window, show="*")
    password_entry.pack(pady=5)

    # 登录按钮
    def login_action():
        username = username_entry.get()
        password = password_entry.get()
        result=get_user_info(username,password)
        if result[0]:
            login_window.destroy()  # 关闭登录窗口
            if get_stock_info():
                root_jk.creat_main_ui()  # 打开主界面
        else:
            messagebox.showerror(result[1].get("message"))

    # 登录按钮
    def create_action():
        username = username_entry.get()
        password = password_entry.get()
        result=create_user_info(username,password)
        if result[0]:
            messagebox.showerror(result[1].get("message"))
        else:
            messagebox.showerror(result[1].get("message"))

    # 登录按钮
    def any_action():
        State_Box.set_state("token", "123")
        if get_stock_info():
            login_window.destroy()  # 关闭登录窗口
            root_jk.creat_main_ui()  # 打开主界面


    button_frame = Frame(login_window)
    button_frame.pack(pady=20, expand=True)  # 使按钮居中并填充

    login_button = Button(button_frame, text="登录", command=login_action)
    create_button = Button(button_frame, text="注册", command=create_action)
    any_button = Button(button_frame, text="游客", command=any_action)
    login_button.pack(side="left", padx=10)
    create_button.pack(side="left", padx=10)
    any_button.pack(side="left", padx=10)

    root.mainloop()