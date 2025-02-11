import hashlib
from flask import Flask, request, jsonify
from tools import get_all_files,get_json_info,set_json_info

app = Flask(__name__)

user_tokens={}
user_tokens["users"] = get_all_files("config")
# 验证 token 是否有效
print(user_tokens)
def verify_token(token):
    # 在实际应用中，可以通过数据库或缓存来验证 token 是否有效
    return token in user_tokens.get("users")


@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# 全局验证 token
@app.before_request
def authenticate():
    if request.path in ['/user/info', '/user/create']:
        return  # 跳过验证
    # 获取请求的 token（可以从请求头、查询参数或请求体中获取）
    token = request.headers.get('Authorization')  # 假设 token 放在请求头的 Authorization 字段
    if not token:
        return jsonify({"code": "2", "message": "缺少 token"})
    # 验证 token
    if not verify_token(token):
        return jsonify({"code": "3", "message": "无效的 token"})

@app.route('/user/info', methods=['POST'])
def get_user_info():
    # 从请求中获取账号和密码
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 验证输入
    if not username or not password:
        return jsonify({"code":"1","message":"缺少账号密码"})

    # 计算密码的 MD5
    password_md5 = hashlib.md5(password.encode('utf-8')+username.encode('utf-8')).hexdigest()
    if password_md5 in user_tokens.get("users"):
        # 返回 MD5 结果
        return jsonify({
            "code": '0',
            'username': username,
            'token': password_md5
        })
    else:
        return jsonify({
            "code": '1',
            "message":"没有账号信息"
        })

@app.route('/user/create', methods=['POST'])
def create_user_info():
    # 从请求中获取账号和密码
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 验证输入
    if not username or not password:
        return jsonify({"code":"1","message":"缺少账号密码"})

    # 计算密码的 MD5
    password_md5 = hashlib.md5(password.encode('utf-8')+username.encode('utf-8')).hexdigest()
    ##创建一个json文件
    if password_md5 in user_tokens.get("users"):
        return jsonify({"code":"1","message":"账号已经存在"})
    else:
        if not password_md5 in get_all_files("config"):
            json_data={
                "update": "3",
                "bk_update": "120",
                "stocks": [{"name": "上证指数","code": "sh000001","cost": "0"}]
            }
            set_json_info(password_md5,json_data)
        user_tokens.get("users").append(password_md5)
        return jsonify({"code":"0","message":f"{username} 用户创建成功"})


@app.route("/get/stock/info", methods=["GET"])
def get_stock_info():
    token = request.headers.get('Authorization')
    if token in user_tokens.get("users"):
        ##读取json文件
        data=get_json_info(token)
        return jsonify({"code":"0","data":data})

@app.route('/config/update', methods=['POST'])
def update_config_info():
    token = request.headers.get('Authorization')
    data = request.get_json()
    change_list = data.get('change_list')
    if token in user_tokens.get("users"):
        json_data = get_json_info(token)
        for change in change_list:
            key = change.get('key')
            new_value = change.get('new_value')
            json_data[key]=new_value
        if set_json_info(token,json_data):
            return jsonify({"code":"0","message":"修改成功"})
        else:
            return jsonify({"code":"0","message":"修改失败"})
    else:
        jsonify({"code": "1", "message": "账号不存在"})

@app.route('/stock/update', methods=['POST'])
def update_stock_info():
    token = request.headers.get('Authorization')
    data = request.get_json()
    code = data.get('code')
    key = data.get('key')
    new_value = data.get('new_value')
    if token in user_tokens.get("users"):
        json_data = get_json_info(token)
        for index,stock_dict in enumerate(json_data["stocks"]):
            if code ==stock_dict.get("code"):
                json_data["stocks"][index][key]=new_value
                break
        if set_json_info(token,json_data):
            return jsonify({"code":"0","message":"修改成功"})
        else:
            return jsonify({"code":"0","message":"修改失败"})
    else:
        return jsonify({"code": "1", "message": "账号不存在"})

@app.route('/stock/add', methods=['POST'])
def add_stock_info():
    token = request.headers.get('Authorization')
    data = request.get_json()
    code = data.get('code')
    name = data.get('name')
    cost = data.get('cost')
    if token in user_tokens.get("users"):
        json_data = get_json_info(token)
        if not json_data.get("stocks"):
            json_data["stocks"]=[]
        for stock in json_data["stocks"]:
            if name in stock.get("name"):
                return jsonify({"code": "1", "message": "自选股中存在这只股票"})
        json_data["stocks"].append({"name": name,"code": code,"cost": cost})
        if set_json_info(token,json_data):
            return jsonify({"code":"0","message":"修改成功"})
        else:
            return jsonify({"code":"0","message":"修改失败"})
    else:
        return jsonify({"code": "1", "message": "账号不存在"})

@app.route('/stock/del', methods=['POST'])
def del_stock_info():
    token = request.headers.get('Authorization')
    data = request.get_json()
    code = data.get('code')
    if token in user_tokens.get("users"):
        json_data = get_json_info(token)
        if not json_data.get("stocks"):
            json_data["stocks"]=[]
            return jsonify({"code":"0","message":"修改失败"})
        for index,stock_dict in enumerate(json_data["stocks"]):
            if code ==stock_dict.get("code"):
                del json_data["stocks"][index]
        if set_json_info(token,json_data):
            return jsonify({"code":"0","message":"修改成功"})
        else:
            return jsonify({"code":"0","message":"修改失败"})
    else:
        return jsonify({"code": "1", "message": "账号不存在"})


@app.route('/get/stock/a', methods=['GET'])
def get_stocks():
    stocks=get_json_info("A_stock")
    if stocks:
        return jsonify(stocks)
    else:
        return jsonify({})




# if __name__ == '__main__':
#     # get_A_stocks()
#     app.run("0.0.0.0",port=8080,debug=False)