#coding: utf-8

__author__ = 'yongfengxia'

import time
from datetime import datetime
import pyodbc


class odbc_sqlserver(object):
    def __init__(self, driver, server, user, passwd, dbname):
        self.params = "DRIVER=%s;SERVER=%s;PORT=1433;DATABASE=%s;UID=%s;PWD=%s;TDS_Version=8.0;" % (
            driver, server, dbname, user, passwd)
        self.connection = pyodbc.connect(self.params)
        self.cursor = self.connection.cursor()

    def fetch_err_log_for_email(self):
        today = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        yesterday = time.strftime("%Y-%m-%d", time.localtime(time.time() - 24 * 3600))

        today_first_msecond = today + " 00:00:00"
        yesterday_first_msecond = yesterday + " 00:00:00"

        sql = "SELECT Host, IP, MonitorTime, AppPath, FirstCag, SecondCag, ThirdCag, ForthCag FROM dbo.LogMinute \
        WHERE MonitorTime >= ? AND MonitorTime < ? AND MonitorAction='Error'"
        self.cursor.execute(sql, datetime.strptime(yesterday_first_msecond, "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime(today_first_msecond, "%Y-%m-%d %H:%M:%S"))
        error_items = list()
        for row in self.cursor:
            error_items.append(
                {'Host': row.Host, 'IP': row.IP, 'MonitorTime': row.MonitorTime, 'AppPath': row.AppPath,
                 'FirstCag': row.FirstCag.decode('gbk'),
                 'SecondCag': row.SecondCag.decode('gbk'), 'ThirdCag': row.ThirdCag.decode('gbk'),
                 'ForthCag': row.ForthCag.decode('gbk')})
        return yesterday, error_items


if __name__ == '__main__':
    odbc_obj = odbc_sqlserver("FreeTDS", "xxx.xxx.xxx.xxx", "wh_sh_ics", "sh_icson%2006", "Monitors")
    results = odbc_obj.fetch_err_log_for_email()
    for index in xrange(10):
        print results[index]['FirstCag']
        print(len(results))
    odbc_obj.cursor.close()
    odbc_obj.connection.close()
