from utils.db_handler import DB

def get_rely_data(case_id, rely_list, request_data):
    """
    从数据库获取存储的依赖数据，然后进行依赖数据处理
    """
    db = DB()
    # 获取已经存储好的依赖数据，字典对象
    rely_data = db.get_rely_data(case_id)
    req_data = request_data.copy()
    for key in rely_list:
        if key in rely_data:
            # 将即将处理依赖的参数名切割出来
            p_key = key.split(".")[-1]
            # 必须要判断一下需要处理的参数是否存在依赖数据中
            req_data[p_key] = rely_data[key]
    return req_data

if __name__ == "__main__":
    r_data = {"username":"lily", "password":"ssd32de2"}
    rely_list = ["request.register.1.username","request.register.1.password"]
    print(get_rely_data(1, rely_list, r_data))