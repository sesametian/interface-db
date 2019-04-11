from utils.db_handler import DB
from action.get_rely import get_rely_data
from utils.HttpClient import HttpClient
from action.data_store import rely_data_store
from action.check_result import CheckResult
from utils.md5_encrypt import md5_encrypt

def main():
    db = DB()
    apiList = db.get_api_list()
    print(apiList)
    for api in apiList:
        api_case_list = db.get_api_case(api[0])
        for case in api_case_list:
            rely_lsit = case[3]
            print(type(rely_lsit))
            request_data = eval(case[2])
            # 接下俩进行数据依赖处理
            if rely_lsit:
                rely_lsit = eval(rely_lsit)
                rely_case_id = rely_lsit[0].split(".")[2]
                request_data = get_rely_data(rely_case_id, rely_lsit, request_data)
            # 特殊处理一下密码加密
            if api[2] == "users_login":
                request_data["password"] = md5_encrypt(request_data["password"])
            # 接下来进行接口请求，并获取响应body
            responseObj = HttpClient.request(api[3], api[4], api[5], request_data)
            print(responseObj.status_code)
            # 接下来进行数据依赖存储
            if responseObj.status_code == 200 and responseObj.json()["code"] == "00" and case[6]:
                rely_data_store(api[0], case[0], api[1], eval(case[6]), request_data, responseObj.json())
            # 接下来进行接口响应结果验证
            errorInfo = CheckResult.check(responseObj.json(), eval(case[7]))
            print(errorInfo)
            db.write_check_result(case[0], errorInfo, request_data)


if __name__ == "__main__":
    main()