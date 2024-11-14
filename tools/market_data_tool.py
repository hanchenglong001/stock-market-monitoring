from requests import get
from config import init_conf



# 获取多个股票的实时数据
def get_stock_data(stocks):
    stock_urls = {}
    stock_ben = {}
    for name in stocks:
        stockvlue = init_conf.get_value("stock", name)
        _ = stockvlue.split(";")
        stock = _[0]
        stock_ben[name] = _[1] if len(_) > 1 else 0
        stock_urls[name] = f"https://hq.sinajs.cn/list={stock}"

    headers = {"Referer": "https://finance.sina.com.cn"}
    stock_data = {}
    for stock_name, url in stock_urls.items():
        response = get(url, headers=headers)
        data = response.text.split(",")
        if len(data) > 30:
            current_index = data[3]
            yesterday_index = data[2]
            stock_data[stock_name] = [current_index, stock_ben.get(stock_name), yesterday_index]
        else:
            stock_data[stock_name] = f"{stock_name}: 无法获取数据"
    return stock_data



# 获取多个股票的实时数据
def get_one_stock_data(stock):
    stock_urls = {}
    stock_ben = {}
    for name in [stock]:
        stockvlue = init_conf.get_value("stock", name)
        _ = stockvlue.split(";")
        stock = _[0]
        stock_ben[name] = _[1] if len(_) > 1 else 0
        stock_urls[name] = f"https://hq.sinajs.cn/list={stock}"

    headers = {"Referer": "https://finance.sina.com.cn"}
    stock_data = {}
    stock_name = ''
    for stock_name, url in stock_urls.items():
        response = get(url, headers=headers)
        data = response.text.split(",")
        if len(data) > 30:
            current_index = data[3]
            yesterday_index = data[2]
            stock_data[stock_name] = [current_index, stock_ben.get(stock_name), yesterday_index]
        else:
            stock_data[stock_name] = f"{stock_name}: 无法获取数据"
    return stock_data[stock_name]