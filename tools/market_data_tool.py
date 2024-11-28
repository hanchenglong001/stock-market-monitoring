import requests


# 统一获取股票数据的函数
def fetch_stock_data(stock_symbol):
    url = f"https://hq.sinajs.cn/list={stock_symbol}"
    headers = {"Referer": "https://finance.sina.com.cn"}
    response = requests.get(url, headers=headers)
    return response.text.split(",")


# 获取多个股票的实时数据
def get_stock_data(stocks):
    ##查看如此是否是list
    if not isinstance(stocks, list):
        stocks = [stocks]
    stock_data = {}
    for stock_one in stocks:
        if not isinstance(stock_one, dict):
            stock_one=eval(stock_one)
        stock_symbol=stock_one.get("code")
        stock_name=stock_one.get("name")
        stock_ben=stock_one.get("cost")
        # 获取股票数据
        data = fetch_stock_data(stock_symbol)
        # 解析数据
        if len(data) > 30:
            current_index = data[3]
            yesterday_index = data[2]
            stock_data[stock_name] = [current_index, stock_ben, yesterday_index]
        else:
            stock_data[stock_name] = f"{stock_name}: 无法获取数据"

    return stock_data

