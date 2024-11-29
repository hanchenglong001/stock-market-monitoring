from tools.state_manager import State_Box
import requests

# url='http://10.15.48.250:8080'
url='https://349563332.pythonanywhere.com'

def get_user_info(user,passwd):
    json={
        "username":user,
        "password":passwd,
    }
    result=requests.post(f"{url}/user/info",json=json).json()
    if result.get("code")=="0":
        State_Box.set_state("token",result.get("token"))
        return True,result
    else:
        return False,result

def create_user_info(user,passwd):
    json={
        "username":user,
        "password":passwd,
    }
    result=requests.post(f"{url}/user/create",json=json).json()
    if result.get("code")=="0":
        return True,result
    else:
        return False,result

def get_stock_info():
    result=requests.get(f"{url}/get/stock/info",headers={"Authorization":State_Box.get_state("token")}).json()
    if result.get("code")=="0":
        stocks = result.get("data").get("stocks")
        ms = result.get("data").get("update")
        bkms = result.get("data").get("bk_update")
        if stocks:
            State_Box.set_state("stocks", stocks)
        if bkms:
            State_Box.set_state("bkms", bkms)
        if ms:
            State_Box.set_state("ms", ms)
        return True
    else:
        return False

def config_update(change_list):
    result=requests.post(f"{url}/config/update",headers={"Authorization":State_Box.get_state("token")},json={"change_list":change_list}).json()
    if result.get("code")=="0":
        return True
    else:
        return False


def get_a_stock() -> dict:
    result=requests.get(f"{url}/get/stock/a",headers={"Authorization":State_Box.get_state("token")}).json()
    return result

def add_stock(code,name,cost="0"):
    json_data={
        "code":code,
        "name":name,
        "cost":cost
    }
    result=requests.post(f"{url}/stock/add",headers={"Authorization":State_Box.get_state("token")},json=json_data).json()
    if result.get("code")=="0":
        return True,result
    else:
        return False,result

def del_stock(code):
    json_data={
        "code":code
    }
    result=requests.post(f"{url}/stock/del",headers={"Authorization":State_Box.get_state("token")},json=json_data).json()
    if result.get("code")=="0":
        return True,result
    else:
        return False,result