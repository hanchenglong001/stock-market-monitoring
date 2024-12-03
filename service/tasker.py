import akshare as ak
from service.tools import set_json_info


def get_A_stocks():
    # 获取所有 A 股的股票代码
    stock_list = ak.stock_zh_a_spot()
    # 创建一个字典，键为股票代码，值为股票名称
    stock_dict = {row['代码']: row['名称'] for _, row in stock_list.iterrows()}
    set_json_info("A_stock",stock_dict)

if __name__ == '__main__':
    get_A_stocks()