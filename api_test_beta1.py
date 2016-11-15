# -*- coding: utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import xlrd
import requests
import json
import os
import time
import MySQLdb
import hashlib

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
        #file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
        try:
            data = xlrd.open_workbook(file)
            return data
        except Exception,e:
            print str(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
#将excel表中的数据，遍历放进list
    def excel_table_byindex(self,file,colnameindex=0,by_index=0):
        #file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
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
        return list

#根据名称获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的  ，by_name：Sheet1名称
#将excel表中的数据，遍历放进list
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

#按sheet序号、或sheetname调用上述两个方法
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
        u'''读取excel用例，将url中需替换的参数替换，并调用apicall方法'''
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        list = self.excel_table_byindex(file)
        print list
        #print list
        num = 1
        for i in list:        
            print '==========NOW RUNNINF APICASE',num,'=============='
            i = eval(str(i))
            num = num +1 
            method = i['method']
            url = str(i['url'])
            #下列数据是从数据库取出来的
            (tokenNumber,orderid,courierid) = self.get_sqldata()
            #orderDay 为查询时间，字符型，格式为  yyyyMMdd ,例如20151213
            #pageSize为每页获取记录条数，整型，默认为 15
            #startIndex为页数偏移量，整型， 默认为 -1
            orderDay = 20151027
            pageSize = 15
            startIndex = -1
            baristaId = 217
            shopId = 16
            #判定url是否有参数需替换
            if '{tokenNumber}' in url:      
                url = url.replace('{tokenNumber}',str(tokenNumber))
            if '{courierid}' in url:
                url = url.replace('{courierid}',str(courierid))
            if '{orderid}' in url:
                url = url.replace('{orderid}',str(orderid))
            if '{orderDay}' in url:
                url = url.replace('{orderDay}',str(orderDay))
            if '{pageSize}' in url:
                url = url.replace('{pageSize}',str(pageSize))
            if '{startIndex}' in url:
                url = url.replace('{startIndex}',str(startIndex))
            print url
            if '{shopId}' in url:
                url = url.repalce('{shopId}',str(shopId))
            if '{baristaId}' in url:
                url = url.repalce('{baristaId}',str(baristaId))

            print url
            
            u'''eval方法用来转换成字典类型'''
            getparams = i['getparams']
            if getparams != '':
                getparams = eval(str(getparams))
            postparams = i['postparams']
            if postparams != '':
                postparams = eval(str(postparams))
            putparams = i['putparams']
            if putparams != '':
                putparams = eval(str(putparams))
            #   status = api_sheet.cell(i,5).value

            data = self.apicall(method,url,getparams,postparams,putparams,headers)
            #codec = 'utf-8'
            #data = data.decode(codec)

            try:
                if data['status'] == 0:
                    print 'pass'
                    print data

                else:
                    print 'case fail'
                    print data
                    print data['message']
                    
                    #print data['message'].encode('gbk')
            except Exception,e:
                print Exception,':',e
                print 'wrong!please check!!!'
                print 'status:',data
                continue

               

if __name__ =='__main__':
    api_case = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case_courier_barista.xlsx'
    a = CallApi()
    a.excel_data(api_case)
    #a.excel_table_byindex(api_case)
    #sha1加密 hashlib.sha1(a).hexdigest()
    '''hash_new = hashlib.sha1() #或hashlib.md5()
with open('driver.xml.tar.bz2','rb') as fp: #打开文件，一定要以二进制打开
    while True:
        data = fp.read() #读取文件块
        if not data: #直到读完文件
            break
        hash_new.update(data)
hash_value = hash_new.hexdigest() #生成40位(sha1)或32位(md5)的十六进制字符串
print hash_value'''
 