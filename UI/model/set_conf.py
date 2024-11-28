from tkinter import Label, Frame, Toplevel, Entry, Button
from tools.state_manager import State_Box
from UI.small_module.labeled_entry import add_labeled_entry
from tools.login_tool import config_update


def create_modify_config_window(root):
    def save_config():
        # 获取输入框中的配置值
        new_update_interval = entry_update_interval.get()
        new_bk_update_interval = entry_bk_update_interval.get()
        # 保存到 State_Box 或者其他持久化存储
        State_Box.set_state("update", new_update_interval)
        State_Box.set_state("bkms", new_bk_update_interval)
        change_list=[
            {"key":"update","new_value":new_update_interval},
            {"key":"bk_update","new_value":new_bk_update_interval},
        ]

        if config_update(change_list):
            # 显示保存成功的提示
            config_info_label.config(text=f"配置已更新:\n更新间隔：{new_update_interval}秒\n备份更新间隔：{new_bk_update_interval}秒")
        else:
            config_info_label.config(text=f"修改失败")

    modify_config_window = Toplevel(root)
    modify_config_window.title("修改配置")
    modify_config_window.geometry("400x300")

    # 创建并布局标签和输入框
    entry_update_interval = add_labeled_entry(modify_config_window, "股票行情间隔:")
    entry_bk_update_interval = add_labeled_entry(modify_config_window, "板块行情间隔:")

    # 默认填充已有的配置值
    entry_update_interval.insert(0, State_Box.get_state("update"))
    entry_bk_update_interval.insert(0, State_Box.get_state("bkms"))

    entry_update_interval.pack()
    entry_bk_update_interval.pack()

    # 保存按钮
    Button(modify_config_window, text="保存配置", command=save_config).pack()

    # 显示当前配置状态的标签
    config_info_label = Label(modify_config_window, text="")
    config_info_label.pack()

