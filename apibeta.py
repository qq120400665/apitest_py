# -*- coding: utf-8 -*- 
import  xdrlib ,sys
import xlrd
import requests
import json
import os
import time
import xlrd
import MySQLdb

class CallApi():
    
    u'''调用接口方法'''
    def apicall(self,method,url,getparams,postparams,putparams,headers):
        result = ''
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        if method == 'GET':
            if getparams != '':
                result = requests.get(url,params=getparams,headers=headers)
            else:
                result = requests.get(url,headers=headers)

        if method == 'POST':
            if postparams != '':
                result = requests.post(url,params=postparams,headers=headers)
            else:
                result = requests.post(url,headers=headers)

        if method == 'PUT':
            if putparams != '':
                result = requests.put(url,params=putparams,headers=headers)
            else:
                result = requests.put(url,headers=headers)

        try:
            jsdata = json.loads(result.text)
            return jsdata
            #print jsdata
        except Exception,e:
            print Exception,':',e
        #print jsdata
        #return jsdata

    def open_excel(slef,file):
        u'''打开excel'''
        file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception,e:
            print str(e)
#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
    def excel_table_byindex(self,file,colnameindex=0,by_index=0):
        file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
        data = self.open_excel(file)
        table = data.sheets()[by_index]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        colnames =  table.row_values(colnameindex) #某一行数据 
        list =[]
        for rownum in range(1,nrows):

            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i] 
                list.append(app)
        
        return table

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的  ，by_name：Sheet1名称
    def excel_table_byname(self,file,colnameindex=0,by_name=u'Sheet1'):
        data = self.open_excel(file)
        table = data.sheet_by_name(by_name)
        nrows = table.nrows #行数 
        colnames =  table.row_values(colnameindex) #某一行数据 
        list =[]
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list.append(app)
        return list

    def main(self):
        tables = self.excel_table_byindex(file)
        for row in tables:
            print row

        tables = self.excel_table_byname(file)
        for row in tables:
            print row

    def get_sqldata(self):
        u'''访问数据库获取token和订单号'''
        db = MySQLdb.connect(host="115.29.208.235",user="dbadmin",passwd="dbadminpass",db="lyancafe",port=3306,charset="utf8")
        cursor = db.cursor()
        cursor.execute("select token from t_user_token where device = 'A000004F0B0A47' order by updated desc limit 1")
        tokenNumber = str(cursor.fetchone()[0])
        cursor.execute("select id from orders where internal_status = '3010' and delivery_area_id = '52' order by csr_handle_time desc limit 1;")
        orderid = str(cursor.fetchone()[0])
        courierid = 214
        return (tokenNumber,orderid,courierid)

    def excel_data(self,file):
        u'''读取excel用例'''
        table = self.excel_table_byindex(file)
        url = str(table.cell(8,1).value)
        print url
        url1 = url.replace('{tokenNumber}','aaaaaaa')
        print url1
               

if __name__ =='__main__':
    api_case = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
    a = CallApi()
    a.excel_data(api_case)
    #a.excel_table_byindex(api_case)
