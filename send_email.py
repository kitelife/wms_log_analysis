#coding: utf-8

import time
from jinja2 import Template

import access_sqlserver
from TofApi import TofApi

APP_KEY = '742f1976c47c494285aa8d6e47daeb70'
SENDER = 'sender@email.com'
RECEIVERS = ['receiver@email.com']

EMAIL_TEMPLATE = u'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>WMS日志统计报告</title>
        <style type="text/css">
            body {
                width:100% !important;
                -webkit-text-size-adjust:100%;
                -ms-text-size-adjust:100%;
                margin:0;
                padding:0;
            }

            table {
                border-collapse: collapse;
                border-spacing:0;
                border:1px solid #000000;
            }

            #table-header {
                background-color: #71D7D7;
                font-weight: bold;
                font-size: 15px;
            }

            .description, .err-num {
                text-align: center;
            }

            .host_part, .ip_part {
                color: #FF0000;
            }

            .app_path_part {
                color: #008500;
            }

            .first_cag_part {
                color: #FF4040;
            }

            .second_cag_part {
                color: #FF7373;
            }

            .third_cag_part {
                color: #FF7400;
            }

            .forth_cag_part {
                color: #A60000;
            }
        </style>
    </head>
    <body style="margin: 0; padding: 0;">
        <table border="1" cellpadding="0" cellspacing="0" width="100%">
        <tr class="description">
            <h2>WMS日志错误统计报告</h2>
        </tr>
        <tr class="description">
            <h4>日期：{{ date }}</h4>
        </tr>
        <tr class="description">
            <h3>错误总数：{{ err_num }}</h3>
        </tr>
        </tr>
        <tr id="table-header">
            <td class="description">机器模块</td>
            <td class="description">错误数目</td>
        </tr>
        {% for (key, value) in items %}
        <tr>
            <td>{{ key }}</td>
            <td class="err-num">{{ value }}</td>
        </tr>
        {% endfor %}
        </table>
    </body>
</html>
'''


def analysis_and_send():
    odbc_obj = access_sqlserver.odbc_sqlserver("FreeTDS", "xxx.xxx.xxx.xxx", "wh_sh_ics", "sh_icson%2006",
                                               "Monitors")
    date, log_data = odbc_obj.fetch_err_log_for_email()
    print len(log_data)
    analysis_dict = {}
    for item in log_data:
        key = "<span class='host_part'>%s</span><span class='ip_part'>(%s)</span> -> <span class='app_path_part'>%s</span> -> \
        <span class='first_cag_part'>%s</span> -> <span class='second_cag_part'>%s</span> -> \
        <span class='third_cag_part'>%s</span> -> <span class='forth_cag_part'>%s</span>" % (
            item["Host"], item["IP"], item["AppPath"], item["FirstCag"], item["SecondCag"], item["ThirdCag"],
            item["ForthCag"])
        if key in analysis_dict:
            analysis_dict[key] += 1
        else:
            analysis_dict[key] = 1
    analysis_list = []
    for key, value in analysis_dict.iteritems():
        analysis_list.append([key, value])
    analysis_list.sort(key=lambda x: x[1], reverse=True)
    template = Template(EMAIL_TEMPLATE)
    email_content = template.render(date=date, err_num=len(log_data), items=analysis_list)
    email_title = u'WMS日志统计报告'
    api = TofApi(APP_KEY)
    receivers = ';'.join(RECEIVERS)
    api.send_mail(SENDER, receivers, email_title.encode('utf-8'), email_content.encode('utf-8'))


if __name__ == '__main__':
    print '*** Begin *** ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    analysis_and_send()
    print '*** End *** ', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print
