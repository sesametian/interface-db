from utils.db_handler import DB

def rely_data_store(api_id, case_id, api_name, store_rule, request_data, response_data):
    data_store_dict = {}
    for key, value in store_rule.items():
        if key == "request":
            for p_name in value:
                if p_name in request_data:
                    # 拼接需要存储的依赖数据的key
                    # rely_key = "%s.%s.%s.%s" %("request", api_name, str(case_id) ,p_name)
                    rely_key = "request." + api_name + "." + str(case_id) + "." + p_name
                    data_store_dict[rely_key] = request_data[p_name]
        elif key == "response":
            for p_name in value:
                if p_name in response_data:
                    # rely_key = "%s.%s.%s.%s" %("request", api_name, str(case_id) ,p_name)
                    rely_key = "response." + api_name + "." + str(case_id) + "." + p_name
                    data_store_dict[rely_key] = response_data[p_name]
    db = DB()
    # 向数据库中写存储依赖数据
    db.write_store_data(api_id, case_id, data_store_dict)
    db.close_connect()
