#encoding=utf-8
import pymysql
from utils.config_handler import ConfigParse

class DB(object):
    def __init__(self):
        self.db_conf = ConfigParse().get_db_conf()
        self.conn = pymysql.connect(
            host = self.db_conf["host"],
            port = int(self.db_conf["port"]),
            user = self.db_conf["user"],
            password = self.db_conf["password"],
            database = self.db_conf["db"],
            charset = "utf8"
        )
        self.cur = self.conn.cursor()

    def close_connect(self):
        # 关闭数据连接
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def get_api_list(self):
        try:
            sqlStr = "select * from interface_api where status=1"
            self.cur.execute(sqlStr)
            # 返回tuple对象
            apiList = list(self.cur.fetchall())
            return apiList
        except Exception as err:
            raise err

    def get_api_case(self, api_id):
        sqlStr = "select * from interface_test_case where api_id=%s and status=1" %api_id
        self.cur.execute(sqlStr)
        api_case_list = list(self.cur.fetchall())
        return api_case_list

    def get_rely_data(self, case_id):
        print(case_id)
        sqlStr = "select data_store from interface_data_store where case_id=%s" %(case_id)
        self.cur.execute(sqlStr)
        # 字典对象
        rely_data = eval((self.cur.fetchall())[0][0])
        return rely_data

    def write_store_data(self, api_id, case_id, data_store):
        print(data_store)
        sqlStr = "select * from interface_data_store where api_id=%s and case_id=%s" %(api_id, case_id)
        self.cur.execute(sqlStr)
        query_result = self.cur.fetchall()
        if query_result:
            sqlStr = "update interface_data_store set data_store=\"%s\" where api_id=%s and case_id=%s" %(data_store, api_id, case_id)
            print(sqlStr)
            self.cur.execute(sqlStr)
            self.conn.commit()
        else:
            sqlStr = "insert into interface_data_store(api_id, case_id, data_store) values(%s, %s, \"%s\")" %(api_id, case_id, data_store)
            print(sqlStr)
            self.cur.execute(sqlStr)
            self.conn.commit()

    def write_check_result(self, case_id, errorInfo, res_data):
        sqlStr = "update interface_test_case set error_info=\"%s\", res_data=\"%s\" where id=%s" %(errorInfo, res_data, case_id)
        self.cur.execute(sqlStr)
        self.conn.commit()


if __name__ == '__main__':
    db = DB()
    # print(db.get_api_list())
    # print(db.get_api_case(1))
    # print(db.get_rely_data(2,2))
    db.write_store_data(1,1, "d")
