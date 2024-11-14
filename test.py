from pystray import Icon, MenuItem
from PIL import Image


# 定义点击菜单项的回调函数
def on_notify(icon, item):
    icon.notify(title="通知标题", message="通知内容")


# 创建图标对象
icon = Icon("Tray Icon", Image.open("your_icon_path.png"), "鼠标移动到\n托盘图标上\n展示内容",
            MenuItem('发送通知', on_notify),
            MenuItem('退出', None, should_exit=True))

# 显示图标并等待用户操作
icon.run()
