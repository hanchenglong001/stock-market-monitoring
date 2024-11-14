def calculate_average_cost(shares_owned,cost_price, current_price, target_cost):

    # 计算当前市值
    current_value = shares_owned * cost_price
    # 目标补仓数量的方程
    # (当前市值 + 当前价格 * 补仓数量) / (持仓数量 + 补仓数量) = 目标成本
    # 变形为：补仓数量 = (目标成本 * (持仓数量 + 补仓数量) - 当前市值) / 当前价格
    # 计算补仓数量
    # 先设定一个初始补仓数量
    x = 0
    while True:
        x += 1  # 逐步增加补仓数量
        total_shares = shares_owned + x
        new_average_cost = (current_value + current_price * x) / total_shares

        if new_average_cost <= target_cost:
            break
    return x



def get_required_shares(shares_owned, cost_price, current_price, target_cost):
    """
    :param shares_owned: 持有股票数量
    :param cost_price: 成本价格
    :param current_price:  当前价格
    :param target_cost: 目标成本
    :return:
    """

    # 当前市值
    shares_owned = float(shares_owned)
    cost_price = float(cost_price)
    current_price = float(current_price)
    target_cost = float(target_cost)

    if current_price >= target_cost:
        return "目标成本无法达成"

    # 计算需要补仓的数量
    required_shares = calculate_average_cost(shares_owned, cost_price, current_price, target_cost)
    return f"需要补仓数量: {required_shares}股 --补仓金额 {round(required_shares* current_price,2)}元,补仓亏损{round((target_cost-current_price)/current_price*100,2)}%"


if __name__ == '__main__':
    # 示例参数
    shares_owned = 1300  # 持有股票数量
    # 成本价格
    cost_price = 10.455  # 成本价格
    current_price = 8.180  # 当前价格
    target_cost = 8.5  # 目标成本
    required_shares = calculate_average_cost(shares_owned, cost_price,current_price, target_cost)
