from config import init_conf
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

    for stock_name in stocks:
        # 获取配置中的股票信息
        stock_value = init_conf.get_value("stock", stock_name)
        stock_symbol, stock_ben = stock_value.split(";", 1) if ';' in stock_value else (stock_value, "0")

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

