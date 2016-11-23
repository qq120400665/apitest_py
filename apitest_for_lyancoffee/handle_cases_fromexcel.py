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
import copy
import configparser


class HandleCasesFromExcel():
    def __init__(self,initfile):
        config = configparser.ConfigParser()
        config.read(initfile)
        self.st = config.get('CASEID','caseid')
        self.names = config.get('NAMES','names')
        self.apicase = config.get('FILE','apicase')


    def open_excel(self,file1):
        u'''打开excel'''
        #file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
        try:
            data = xlrd.open_workbook(file1)
            return data
        except Exception,e:
            print str(e)

#根据索引获取Excel表格中的数据   参数:file：Excel文件路径     colnameindex：表头列名所在行的所以  ，by_index：表的索引
#将excel表中的数据，遍历放进list
    def excel_table_byindex(self,file1,colnameindex=0,by_index=0):
        #file = 'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
        data = self.open_excel(file1)
        table = data.sheets()[by_index]
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        colnames =  table.row_values(colnameindex) #某一行数据
        list1 =[]
        for rownum in range(1,nrows):
            row = table.row_values(rownum)
            if row:
                app = {}
                for i in range(len(colnames)):
                    app[colnames[i]] = row[i]
                list1.append(app)
        return list1

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

    def request_courier_barista(self,file):
        u'''读取excel用例，将url中需替换的参数替换，并调用apicall方法'''
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        list = self.excel_table_byindex(file)
        #print list
        num = 1
        for i in list:
            print '==========NOW RUNNINF APICASE',num,'=============='
            i = eval(str(i))
            num = num +1
            print i
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
                print 'wrongs!!!'
                print 'status:',data
                continue

    def request_the_third_who(self,file,names=None):
        names = names or []
        for name in names:
            result = self.request_the_third(file)
            return result

    def handle_eachcase(self):
        #对excel每天case处理，只保留参数部分
        caselists = self.excel_table_byindex(self.apicase)
        print 'caselists:',json.dumps(caselists,encoding='UTF-8',ensure_ascii=False)
        for caselist in caselists:
            for i in caselist.keys():
                #print type(i)
                #print 'i:',json.dumps(i,encoding='UTF-8',ensure_ascii=False)
                if caselist[i] == '':
                    del caselist[i]
                if i == 'method':
                    del caselist[i]
                if i == 'url':
                    del caselist[i]
                if i == 'status':
                    del caselist[i]
                if i == 'description':
                    del caselist[i]
        caselists_params = caselists
        print 'caselists_params:',json.dumps(caselists_params,encoding='UTF-8',ensure_ascii=False)
        return caselists_params

    def handle_eachcase1(self):
        #将元素{}转为[]
        caselists = self.handle_eachcase(apitest)
        for i in range(0,len(caselists)):
            if caselists[i]=={}:
                caselists[i] = []
        caselists_params1 = caselists
        print 'caselists_params1:',json.dumps(caselists_params1,encoding='UTF-8',ensure_ascii=False)
        return caselists_params1

    def handle_eachparam(self):
        #用=连接各个参数
        caselists_params = self.handle_eachcase()
        eachparam_connect = []
        eachparams_connect = []
        params = []
        for caselists_param in caselists_params:
            if caselists_param != {}:
                for i in caselists_param.keys():
                    eachparam = str(i)+'='+str(caselists_param[i])
                    eachparam_connect.append(eachparam)
                eachparams_connect.append(eachparam_connect)
                eachparam_connect = []
            else:
                eachparams_connect.append([])
        print 'eachparams_connect:',json.dumps(eachparams_connect,encoding='UTF-8',ensure_ascii=False)
        return eachparams_connect

    def handle_sign(self):
        #用appid、appkey和参数生成sign
        nonce = 'nonce='+str(time.time()).split('.')[0]+'000'
        eachparams_connect = self.handle_eachparam()
        sign = []
        n=1
        for eachparam_connect in eachparams_connect:
            for name in eval(self.names):
                print 'name:',type(eval(self.names))
                print '=============handle %s' %(name.keys()) ,'the %sst case' %n ,'======='
                appid = 'appid='+str(name.values()[0][0])
                appkey = 'appkey='+str(name.values()[0][1])
                eachparam_connect.append(nonce)
                eachparam_connect.append(appid)
                eachparam_connect.sort()
                eachparam_connect.append(appkey)
        #print 'eachparam_connect:',eachparam_connect
                sign_ex = '&'.join(eachparam_connect)
                eachsign = hashlib.sha1(sign_ex).hexdigest()
                print 'eachparam_connect:',eachparam_connect
                eachparam_connect.remove(nonce)
                eachparam_connect.remove(appid)
                eachparam_connect.remove(appkey)
                print eachsign
                sign.append(eachsign)
            n+=1
        print 'sign:',sign
        return sign

    def handle_params_withsign(self):
        nonce = str(time.time()).split('.')[0]+'000'
        caselists_params = self.handle_eachcase()
        sign = self.handle_sign()
        params_withsign = []

        n=1
        m = 1
        for i in range(0,len(caselists_params)):
            for name in eval(self.names):
                params = {}
                caselists_params[i]['appid'] = name.values()[0][0]#赋值语句不会创建对象的副本，仅仅创建引用这是Python的一个核心理念，有时候当行为不对时会带来错误。在下面的例子中，一个列表对象被赋给了名为L的变量，然后L又在列表M中被引用。内部改变L的话，同时也会改变M所引用的对象，因为它们俩都指向同一个对象。
                caselists_params[i]['nonce'] = nonce
                #locals()['caselists_params_'+name+'_'+str(n)] = caselists_params[i] #动态变量名
                #print 'caselists_params_'+name+'_'+str(    n) , locals()['caselists_params_'+name+'_'+str(n)]
                params['caselists_params_'+str(name.keys())+'_'+str(n)] = caselists_params[i]
                params_ = copy.deepcopy(params)#创建副本，避免被引用
                params_withsign.append(params_)
                print 'params_withsign',params_withsign
            n+=1
        print 'params_withsign_ex:',params_withsign
        print len(params_withsign)
        for i in range(0,len(params_withsign)):
            for j in range(0,len(sign)):
                if i ==j:
                    params_withsign[i].values()[0]['sign'] = sign[j]


        print 'params_withsign:',json.dumps(params_withsign,encoding='UTF-8',ensure_ascii=False)
        return params_withsign

    def handle_caseid(self):
        #按输入处理指定的case：2或者2,3或者ALL
        params = self.handle_params_withsign()
        n = len(params)/len(eval(self.names))
        case_id = []
        cases = []
        while True:
            print u'共有'+ str(n) + u'条用例'
            # st = raw_input(u'请输入想运行的用例编号，比如2或者2,3或者ALL：')
            #print type(st)
            if len(self.st) != 0:
                break
        if self.st == 'all' or self.st == 'ALL':
            pass#逐个请求接口
            for  i in params:
                case_id.append(i.keys()[0].split('_')[-1])
                cases.append(i)
        else:
            self.st = self.st.split(',')
            for i in self.st:
                for j in params:
                    if str(i) == j.keys()[0].split('_')[-1]:
                        #print i
                        case_id.append(i)
                        #print j
                        cases.append(j)
                        #pass #执行请求接口.
        caselists = self.excel_table_byindex(self.apicase)
        methods = []
        urls = []
        for i in case_id:
            methods.append(caselists[int(i)-1]['method'])
            urls.append(caselists[int(i)-1]['url'])
        print 'methods:',methods
        print 'urls:',urls
        print 'case_id:',case_id
        print 'cases:',json.dumps(cases,encoding='UTF-8',ensure_ascii=False)
        return methods,urls,case_id,cases



    def compare_status(self):
        pass


# if __name__ =='__main__':
#     # names=[{'app_qusong':['e2beb30fe93cd5ca9ed0ba705a4e6096','4252855545bfabcf39a7d7d2ea7e268b9925d81e']},
#     # {'app_wokuaidao':['9c838579adda7f729382e226459340e3','7fd154b4fa0afa268f607dde2c381703aa108c21']},
#     # {'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']},
#     # {'app_sweets':['9fde23f821e48ddb20164374957ef772','36412135402bc7d6821781dcc10e5b25abc1ab00']},
#     # {'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}]
#
# #     #names={'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
# #     #names={'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}
# #     #names={'app_chubao':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
#
# if __name__ == '__main__':
#     a = HandleCasesFromExcel('./case_config.ini')
#     a.handle_caseid()
#         #input("Prease <enter>")

#     '''hash_new = hashlib.sha1() #或hashlib.md5()
# with open('driver.xml.tar.bz2','rb') as fp: #打开文件，一定要以二进制打开
#     while True:
#         data = fp.read() #读取文件块
#         if not data: #直到读完文件
#             break
#         hash_new.update(data)
# hash_value = hash_new.hexdigest() #生成40位(sha1)或32位(md5)的十六进制字符串
# print hash_value'''


