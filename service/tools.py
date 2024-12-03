import os,json

def get_all_files(directory):
    # 获取目录下所有的文件名（不包括子目录）
    file_names = []
    for filename in os.listdir(directory):
        # 获取完整路径
        full_path = os.path.join(directory, filename)
        if os.path.isfile(full_path):  # 如果是文件（而非文件夹）
            file_names.append(filename.replace(".json",""))
    return file_names


def get_json_info(path):
    ###获取json文件，然后修改覆盖原来的
    with open(f'config/{path}.json', 'r', encoding="utf-8") as f:
        content = f.read()
        if not content:  # 文件为空
            return {}
        data = json.loads(content)
        return data

def set_json_info(path,json_data):
    try:
        with open(f'config/{path}.json', 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)  # 将数据写回文件
        return True
    except Exception:
        return False