from tools.state_manager import State_Box


# 定义点击菜单项的回调函数
def notify_box(self, icon, item):
    if item == "h":
        icon.notify(title="预警上限", message="老板发财了")
        State_Box.set_state("yj_h_status", 1)
    if item == "l":
        icon.notify(title="预警下限", message="老板准备跑路了")
        State_Box.set_state("yj_l_status", 1)