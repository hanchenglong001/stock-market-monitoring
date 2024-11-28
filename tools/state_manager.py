class StateManager_Box:
    _instance = None  # 用于保存类的唯一实例

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # 初始化时只需要在第一次实例化时执行
        if not hasattr(self, '_initialized'):
            self._states = {}  # 用于存储所有状态
            self._history = []  # 可选，存储状态变化历史
            self._initialized = True

            ##预警上限
            self.set_state("hjg_value", 0)
            ##预警上限状态
            self.set_state("yj_h_status", 0)
            ##预警下限
            self.set_state("ljg_value", 0)
            ##预警下限状态
            self.set_state("yj_l_status", 0)
            ##窗口可见状态
            self.set_state("window_state", 1)

            self.set_state("update", 3)
            self.set_state("bkms", 120)

        else:
            # 如果已经初始化过，则不执行初始化代码
            print("实例化过了")

    def set_state(self, key, value):
        """设置一个新的状态或更新已有状态"""
        self._states[key] = value
        self._history.append((key, value))  # 可选，记录历史

    def get_state(self, key):
        """获取某个状态的值"""
        return self._states.get(key, None)

    def update_state(self, key, value):
        """更新某个状态值"""
        if key in self._states:
            self._states[key] = value
            self._history.append((key, value))  # 记录更新历史
        else:
            print(f"状态 '{key}' 不存在，请先使用 set_state 添加它。")

    def get_history(self):
        """获取状态变化历史"""
        return self._history

    def remove_state(self, key):
        """删除一个状态"""
        if key in self._states:
            del self._states[key]
            print(f"状态 '{key}' 已被删除。")
        else:
            print(f"状态 '{key}' 不存在。")

    def clear_states(self):
        """清空所有状态"""
        self._states.clear()
        self._history.clear()  # 清空历史记录


State_Box = StateManager_Box()
