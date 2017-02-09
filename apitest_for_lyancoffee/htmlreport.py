#!/usr/bin/env python
# -*- coding:utf-8 -*-

__author__ = 'Salyu'

from pyh import *
import time
import os
from request_eachcase import ApiCall
from response_assert import ResponseAssert
import json



class HtmlReport:
    def __init__(self):
        self.title = 'test_report_page'   # 网页标签名称
        self.filename = ''                   # 结果文件名
        self.time_took = '00:00:00'         # 测试耗时
        self.success_num = 0                  # 测试通过的用例数
        self.fail_num = 0                     # 测试失败的用例数
        self.error_num = 0                    # 运行出错的用例数
        self.case_total = 0                   # 运行测试用例总数
        a = ApiCall()
        result = a.request_eachcase()         #获取测试结果
        b = ResponseAssert('./case_config.ini')
        (self.data_report,self.success_num,self.fail_num,self.case_total) = b.handle_for_report()

    # 生成HTML报告
    def generate_html(self):
        page = PyH(self.title)
        page << h1('test report', align='center') # 标题居中

        page << p('测试总耗时：' + self.time_took)

        page << p('测试用例数：' + str(self.case_total) + '&nbsp'*10 + '成功用例数：' + str(self.success_num) +
                      '&nbsp'*10 + '失败用例数：' + str(self.fail_num) + '&nbsp'*10 +  '出错用例数：' + str(self.error_num))
        #  表格标题caption 表格边框border 单元边沿与其内容之间的空白cellpadding 单元格之间间隔为cellspacing

        tab = table( border='1', cellpadding='1', cellspacing='0', cl='table')
        tab1 = page << tab
        tab1 << tr(td('用例ID', bgcolor='#ABABAB',align='center')+ td('接口描述',bgcolor='#ABABAB', align='center')+ td('请求方法',bgcolor='#ABABAB', align='center') + td('请求URL',bgcolor='#ABABAB',align='center')+td('请求参数/数据', bgcolor='#ABABAB',align='center')+td('测试方法',bgcolor='#ABABAB',align='center')+ td('测试结果', bgcolor='#ABABAB', align='center')+td('返回值',bgcolor='#ABABAB',align='center'))

        # 查询所有测试结果并记录到html文档
        # query = ('SELECT case_id, http_method, request_name, request_url,'
        #               'request_param, test_method, test_desc, result, reason FROM test_result')
        # self.cursor.execute(query)
        # query_result = self.cursor.fetchall()
        for row in self.data_report:
            # print 'row:',row
            if row[6] == 'Pass':
                tab1<< tr(td(row[0], align='center') + td(row[1]) +
                              td(row[2]) + td(row[3], align='center') +
                              td(json.dumps(row[4],encoding='UTF-8',ensure_ascii=False).replace('\\','')) +td(json.dumps(row[5],encoding='UTF-8',ensure_ascii=False))+ td(row[6]) + td(json.dumps(row[7],encoding='UTF-8',ensure_ascii=False).replace('\\','')))
            else:
                tab1<< tr(td(row[0], align='center') + td(row[1]) +
                              td(row[2]) + td(row[3], align='center') +
                              td(json.dumps(row[4],encoding='UTF-8',ensure_ascii=False).replace('\\','')) + td(json.dumps(row[5],encoding='UTF-8',ensure_ascii=False))+td(row[6],bgcolor='#FF0000') + td(json.dumps(row[7],encoding='UTF-8',ensure_ascii=False).replace('\\','')))
        # self._set_result_filename(file)
        report = os.listdir(r'C:\\Users\\lyancoffee\\Desktop\\apitest\\apitest_for_lyancoffee\\report')
        report_num = len(report)
        now = time.strftime('%Y-%m-%d_%H_%M_%S',time.localtime())
        filename = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\apitest_for_lyancoffee\\report\\'+now+'&'+str(report_num+1)+'.html'
        page.printOut(filename)

        # try:
        #     pass
        # except Exception as e:
        #     print('%s' % e)



    # 设置结果文件名
    def _set_result_filename(self, filename):
        self.filename = filename
        #判断是否为目录
        if os.path.isdir(self.filename):
            raise IOError("%s must point to a file" % path)
        elif '' == self.filename:
            raise IOError('filename can not be empty')
        else:
            parent_path, ext = os.path.splitext(filename)
            tm = time.strftime('%Y%m%d%H%M%S', time.localtime())
            self.filename = parent_path + tm + ext

    # 统计运行耗时
    def set_time_took(self, time):
        self.time_took = time
        return self.time_took

if __name__ == '__main__':
    a = HtmlReport()
    a.generate_html()
