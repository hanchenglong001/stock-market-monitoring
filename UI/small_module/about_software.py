from tkinter import Label, Toplevel
import webbrowser

##作者
name="hcl"
##版本
version="v0.01"
##项目地址
url="https://gitee.com/gcggcg/stock-market-monitoring"


def software_info(root):
    # 创建一个子窗口
    about_window = Toplevel(root)
    about_window.title("关于")
    # 设置窗口大小和位置
    about_window.geometry("200x150")
    # 确保子窗口无法调整大小
    about_window.resizable(False, False)
    # 在窗口中添加一个标签，显示软件信息
    about = Label(about_window, text=version)
    about.pack(pady=10)  # 添加一定的上下间距

    # 显示超链接
    def open_url():
        webbrowser.open(url)
    # 可根据需要添加其他内容
    Label(about_window, text=name).pack()
    link_label =Label(about_window, text="项目地址",fg="blue",cursor="hand2")
    link_label.pack(pady=10)
    # 绑定点击事件
    link_label.bind("<Button-1>", lambda e: open_url())