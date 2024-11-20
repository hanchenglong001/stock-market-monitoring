import json
import random
import time
import requests

def generate_jsonp_callback():
    timestamp = int(time.time() * 1000)
    random_number = random.randint(1000000000000000000, 9999999999999999999)
    return f"jQuery{random_number}_{timestamp}"

def get_bk_info():
    url = "https://34.push2.eastmoney.com/api/qt/clist/get"
    dict_bk = {
        'f2': '最新价',
        'f3': '涨跌幅（百分比）',
        'f4': '涨跌值',
        'f5': '成交量（手）',
        'f6': '成交额（元）',
        'f7': '今开',
        'f8': '昨收',
        'f9': '最高价',
        'f10': '最低价',
        'f11': '振幅',
        'f12': '行业代码',
        'f13': '行业级别',
        'f14': '行业名称',
        'f15': '52周最高价',
        'f16': '52周最低价',
        'f17': '5日均价',
        'f18': '10日均价',
        'f20': '流通市值',
        'f21': '总市值',
        'f22': '换手率',
        'f23': '市盈率',
        'f24': '市净率',
        'f25': '总股本（亿）',
        'f26': '成立日期',
        'f33': '保留字段',
        'f62': '营业收入（元）',
        'f104': '成员个数',
        'f105': '成员涨幅大于7%的个数',
        'f107': '成员涨幅大于5%的个数',
        'f115': '保留字段',
        'f124': '数据更新时间',
        'f128': '领涨股票名称',
        'f140': '领涨股票代码',
        'f141': '领涨股票涨跌幅',
        'f136': '领涨股票最新价',
        'f152': '领涨股票成交量（手）',
        'f207': '成分股名称',
        'f208': '成分股代码',
        'f209': '成分股涨跌幅',
        'f222': '成分股涨跌值'
    }
    params = {
        'cb': generate_jsonp_callback(),
        'pn': '1',
        'pz': '90',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'dect': '1',
        'wbp2u': '|0|0|0|web',
        'fid': 'f3',
        'fs': 'm:90+t:2+f:!50',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152,f124,f107,f104,f105,f140,f141,f207,f208,f209,f222',
        '_': int(time.time() * 1000)
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'qgqp_b_id=57b71b155c87ba75bd9043ba2f3468fc; HAList=ty-1-601519-^%^u5927^%^u667A^%^u6167^%^2Cty-1-600419-^%^u5929^%^u6DA6^%^u4E73^%^u4E1A^%^2Cty-1-000001-^%^u4E0A^%^u8BC1^%^%^u6307^%^u6570; st_si=00746454788321; st_asi=delete; st_pvi=00730241331356; st_sp=2024-09-20^%^2009^%^3A24^%^3A00; st_inirUrl=https^%^3A^%^2F^%^2Fwww.baidu.com^%^2Flink; st_sn=26; st_psi=20241120144554158-113200313002-9136060326',
        'Pragma': 'no-cache',
        'Referer': 'https://quote.eastmoney.com/center/boardlist.html',
        'Sec-Fetch-Dest': 'script',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    jsonp_str = requests.get(url, headers=headers, params=params).text
    start_index = jsonp_str.find('(') + 1
    json_data = jsonp_str[start_index:-2]
    json_data = json.loads(json_data).get("data").get("diff")
    # 替换键名为中文含义
    f_bk_info = []
    for bk in json_data:
        chinese_data = {dict_bk[key]: value for key, value in bk.items() if key in dict_bk}
        # 打印替换后的数据
        f_bk_info.append(chinese_data)
    return f_bk_info

if __name__ == '__main__':
    for i in get_bk_info():
        print(i)