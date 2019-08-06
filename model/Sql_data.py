import pymysql
class DB_Operation(object):
    dict_dbs = {}
    dbconn = None
    curdb = None

    dict = {'user': 'root', 'host': 'localhost', 'port': 3306, 'passwd': '123456',
            'db': 'jupyter_on_openshift'}
    dict_dbs['localhost'] = dict

    def __init__(self, source='localhost'):
        user = self.dict_dbs[source]['user']
        host = self.dict_dbs[source]['host']
        port = self.dict_dbs[source]['port']
        passwd = self.dict_dbs[source]['passwd']
        dbname = self.dict_dbs[source]['db']
        self.dbconn = pymysql.connect(host=host, port=port, user=user, passwd=passwd,db=dbname,charset='utf8')
        self.curdb = self.dbconn.cursor(pymysql.cursors.SSCursor)

    def exec_sql(self, sql):
        try:
            self.curdb.execute(sql)
            # 如果是select语句则需要返回
            rs_all = self.curdb.fetchall()
            self.dbconn.commit()
            self.dbconn.close()
            return rs_all
        except Exception as e:
            print ("\n%s \n Exec sql failed, the Exception is %s " % (sql, e))
            self.dbconn.rollback()
            self.dbconn.close()
            exit(1)

#获取登录用户信息
def get_userdata(user_name, pwd):
    dbo = DB_Operation()
    # 数据库读取的登录用户信息
    sql = """select * from tbl_jupyter_user
            where `user` ='%s'  and pwd='%s' 
            """ % (user_name, pwd)
    context = dbo.exec_sql(sql)
    return  context

if __name__=='__main__':
    info_user=get_userdata('wangda','123')
    print (len(info_user))
