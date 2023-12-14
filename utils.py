import json
import os
def read_data_from_json(data_json_path):
    assert os.path.exists(data_json_path), "Error json path: {}".format(data_json_path)
    with open(data_json_path, "r", encoding='utf-8') as json_file:
        data_list = json.load(json_file)
    return data_list

def write_data_to_json(data_json_path, data):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open(data_json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

def txt_to_json(txt_file_path, json_file_path):
    # 读取txt文件并将每行的字典按顺序存储到列表中
    with open(txt_file_path, 'r', encoding='utf-8') as txt_file:
        dict_list = [json.loads(line.strip()) for line in txt_file]

    # 将列表写入json文件
    with open(json_file_path, 'w') as json_file:
        json.dump(dict_list, json_file, indent=2)