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


class HandleCasesFromExcel():
    
    u'''调用接口方法'''
    def apicall(self,method,url,params,headers):
        result = ''
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        if method == 'GET':
            if params != '':
                result = requests.get(url,params,headers=headers)
            else:
                result = requests.get(url,headers=headers)

        if method == 'POST':
            if params != '':
                result = requests.post(url,params,headers=headers)
            else:
                result = requests.post(url,headers=headers)

        if method == 'PUT':
            if params != '':
                result = requests.put(url,params,headers=headers)
            else:
                result = requests.put(url,headers=headers)

        try:
            #jsdata = json.loads(result.text)
            #return jsdata
            #print jsdata
            #print result.encoding
            result.encoding = 'utf-8'
            jsdata = result.json()
            jsdata = json.dumps(jsdata).decode('unicode-escape')
            return jsdata
        except Exception,e:
            print Exception,':',e
        #print jsdata
        #return jsdata

    def open_excel(slef,file1):
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

    '''def request_the_third(self,file1,names=None):
        '''u'处理case里的各项参数，并request''''
        names = names or []
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        list1 = self.excel_table_byindex(file1)
        nonce = str(time.time()).split('.')[0]+'000'
        nonce_ex = 'nonce='+str(time.time()).split('.')[0]+'000'
        n = 1
        for i in list1:
            i = eval(str(i))
            #print i
            method = i['method']
            url = str(i['url'])
            if 'http://apitest.lyancafe.com/third/v1/citys' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split('.')[0]+'000'
                    sign_ex = 'appid='+names[name][0]+ '&'+ nonce_ex +'&' + 'appkey='+ names[name][1]
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    #print sign
                    getparams = {'appid':names[name][0],'nonce':nonce,'sign':sign}
                    print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == '0':
                            print 'pass'
                            print response


                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1

            if 'http://apitest.lyancafe.com/third/v1/provider/goods' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'appid='+names[name][0]+ '&' +  nonce_ex + '&'+ 'providerId=' + str(int(i['provider_id'])) +'&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    #print sign
                    getparams = {'appid':names[name][0],'nonce':nonce,'providerId':int(i['provider_id']),'sign':sign}
                    #print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == '0':
                            print 'pass'
                            print response
                            #print response['data'][0]['subcats'][0]['items']
                            #for i in response['data'][0]['subcats'][0]['items']:
                                #print i['title']



                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
            if 'http://apitest.lyancafe.com/third/v1/expectedtimes' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'address='+ str(i['address']) + '&' +  'appid='+names[name][0]+ '&' + 'city=' + str(i['city']) + '&' +  nonce_ex + '&' +'providerid='+str(int(i['provider_id']))+'&' +'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    print nonce
                    getparams = {'appid':names[name][0],'nonce':nonce,'address':str(i['address']),'sign':sign,'city':str(i['city']),'providerid':str(int(i['provider_id']))}
                    #print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == '0':
                            print 'pass'
                            print json.dumps(response['data']).decode('unicode-escape')
                            #print response['data'][0]['title'].decode('utf-8')
                            #print response['data']
                            #for i in response['data']:
                                #print i['id'],i['select'],i['title']


                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
            if 'http://apitest.lyancafe.com/third/v2/orders/create' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'appid='+names[name][0]+ '&' + 'data=' + str(i['data']) + '&' +  nonce_ex + '&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    postparams = {'appid':names[name][0],'nonce':nonce,'sign':sign,'data':i['data']}
                    print postparams
                    getparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == '0':
                            print 'pass'
                            print response
                            print 111111



                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
                #input("Prease <enter>")
            if 'http://apitest.lyancafe.com/third/v1/order/create' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'appid='+names[name][0]+ '&' + 'data=' + str(i['data']) + '&' +  nonce_ex + '&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    postparams = {'appid':names[name][0],'nonce':nonce,'sign':sign,'data':i['data']}
                    print postparams
                    getparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == '0':
                            print 'pass'
                            print response
                            print 111111



                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
                #input("Prease <enter>")
            if 'http://apitest.lyancafe.com/third/v1/order/inquire' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'appid='+names[name][0] + '&' + nonce_ex + '&' + 'order_id=' + str(int(i['order_id'])) + '&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    getparams = {'appid':names[name][0],'nonce':nonce,'sign':sign,'order_id':int(i['order_id'])}
                    #print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == i['status']:
                            print 'pass'
                            print response

                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
                #input("Prease <enter>")
            if 'http://apitest.lyancafe.com/third/v1/order/check' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print noncenonce_ex = 'nonce='+str(time.time()).split(='.')[0]+'000'
                    sign_ex = 'address='+ str(i['address']) + '&' +  'appid='+names[name][0]+ '&' + 'city=' + str(i['city']) + '&' + 'expectedid=' + str(int(i['expectedid']))+'&'+ nonce_ex + '&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    getparams = {'appid':names[name][0],'nonce':nonce,'address':str(i['address']),'sign':sign,'city':str(i['city']),'expectedid':str(int(i['expectedid']))}
                    print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == i['status']:
                            print 'pass'
                            #print response['data'][0]['title'].decode('utf-8')
                            print response


                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1
            if 'http://apitest.lyancafe.com/third/v1/providers' == i['url']:
                for name in names:
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    #print name
                    sign_ex = 'appid='+names[name][0]+ '&' + 'geo='+i['geo'] + '&' + nonce_ex + '&' + 'appkey='+ names[name][1]
                    #sign_ex = 'appid='+names[name][0]+ '&'+ nonce_ex +'&' + 'appkey='+ names[name][1]
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    #print sign
                    getparams = {'appid':names[name][0],'geo':i['geo'],'nonce':nonce,'sign':sign}
                    #print getparams
                    postparams = ''
                    putparams = ''
                    response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    try:
                        if response['status'] == i['status']:
                            print 'pass'
                            print response['data']
                            for i in response['data']:
                                print i['title']
                                print i['support']


                        else:
                            print 'case fail'
                            print response
                            print response['message']

                    #print data['message'].encode('gbk')
                    except Exception,e:
                        print Exception,':',e
                        print 'wrong!please check!!!'
                        print 'status:',response
                        continue
                n = n+1'''


    def request_the_third_who(self,file,names=None):
        names = names or []
        for name in names:
            result = self.request_the_third(file)
            return result

    def handle_eachcase(self,file1):
        #对excel每天case处理，只保留参数部分
        caselists = self.excel_table_byindex(file1)
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
        caselists = self.handle_eachcase(file1)
        for i in range(0,len(caselists)):
            if caselists[i]=={}:
                caselists[i] = []
        caselists_params1 = caselists
        print 'caselists_params1:',json.dumps(caselists_params1,encoding='UTF-8',ensure_ascii=False)
        return caselists_params1

    def handle_eachparam(self,file1):
        #用=连接各个参数
        caselists_params = self.handle_eachcase(file1)
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

    def handle_sign(self,file1,name=None):
        #用appid、appkey和参数生成sign
        nonce = 'nonce='+str(time.time()).split('.')[0]+'000'
        eachparams_connect = self.handle_eachparam(file1)
        sign = []
        n=1
        for eachparam_connect in eachparams_connect:
            for name in names:
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

    def handle_params_withsign(self,file1,names=None):
        nonce = str(time.time()).split('.')[0]+'000'
        caselists_params = self.handle_eachcase(file1)
        sign = self.handle_sign(file1,names)
        params_withsign = []

        n=1
        m = 1
        for i in range(0,len(caselists_params)):
            for name in names:
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

    def handle_caseid(self,file1,names):
        #按输入处理指定的case：2或者2,3或者ALL
        params = self.handle_params_withsign(file1,names)
        n = len(params)/len(names)
        case_id = []
        cases = []
        while True:
            print u'共有'+ str(n) + u'条用例'
            st = raw_input(u'请输入想运行的用例编号，比如2或者2,3或者ALL：')
            #print type(st)
            if len(st) != 0:
                break
        if st == 'all' or st == 'ALL':
            pass#逐个请求接口
            for  i in params:
                case_id.append(i.keys()[0].split('_')[-1])
                cases.append(i)
        else:
            st = st.split(',')
            for i in st:
                for j in params:
                    if str(i) == j.keys()[0].split('_')[-1]:
                        #print i
                        case_id.append(i)
                        #print j
                        cases.append(j)
                        #pass #执行请求接口.
        caselists = self.excel_table_byindex(file1)
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

    def request_eachcase(self,file1,names):
        #请求接口
        (methods,urls,case_id,cases) = self.handle_caseid(file1,names)
        results = []
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        print case_id
        for i in range(len(case_id)):
            result = {}
            #print methods[i]
            #print urls[i]
            #print cases[i].values()[0]
            response = self.apicall(methods[i],urls[i],cases[i].values()[0],headers)
            #print cases[i].keys()[0]
            result[cases[i].keys()[0]] = response
            #print 'result:',json.dumps(result,encoding='UTF-8',ensure_ascii=False)
            results.append(result)
        #print 'results:',json.dumps(results,encoding='UTF-8',ensure_ascii=False)
        for i in results:
            print i.keys(),':',json.dumps(i.values(),encoding='UTF-8',ensure_ascii=False)
        return results

    def compare_status(self):
        pass

    # def response_compare(self,file1,names=None):
    #     '''比.较status'''
    #     try:
    #         responses = eval(self.request_the_third_response(file1,names))
    #     except Exception,e:
    #         print 1
    #     #continue
    #     print 'response:',json.dumps(response, encoding='UTF-8', ensure_ascii=False)
    #     print 'response[status]:',response['status']
    #     '''获取excel里的每条case'''
    #     list1 = self.excel_table_byindex(file1)
    #     for i in list1:
    #         try:
    #             if response['status'] == i['status']:
    #                 print 'pass'
    #                 #print response['data'][0]['title'].decode('utf-8')
    #                 print response
	#
	#
    #             else:
    #                 print 'case fail'
    #                 print response
    #                 print response['message']
    #
    #     #print data['message'].encode('gbk')
    #         except Exception,e:
    #             print Exception,':',e
    #             print 'wrong!please check!!!'
    #             print 'status:',response
    #             #continue
                


               

if __name__ =='__main__':
    # names=[{'app_qusong':['e2beb30fe93cd5ca9ed0ba705a4e6096','4252855545bfabcf39a7d7d2ea7e268b9925d81e']},
    # {'app_wokuaidao':['9c838579adda7f729382e226459340e3','7fd154b4fa0afa268f607dde2c381703aa108c21']},
    # {'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']},
    # {'app_sweets':['9fde23f821e48ddb20164374957ef772','36412135402bc7d6821781dcc10e5b25abc1ab00']},
    # {'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}]
    api_case = 'c:\\Users\\lyancoffee\\Desktop\\apitest\\api_case_the_third.xlsx'
    #names={'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
    #names={'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}
    #names={'app_chubao':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
    names = [{'app_ali':['dbc1e0a09f15cac4cabf38ed5c0d5974','7e5c0e6a82e026588f4abf02260fa7c3']},{'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}]
    a = HandleCasesFromExcel()
    #if 'courier_barista' in api_case:
        #a.request_courier_barista(api_case)
        #input("Prease <enter>")
    #if 'the_third' in api_case:
        #a.request_the_third(api_case,names)
        #input("Press <enter>")
    #a.handle_urlmethod(api_case,names)
    a.request_eachcase(api_case,names)
        #a.response_compare(api_case,names)
        # a.handle_sign(api_case,names)
        #input("Prease <enter>")
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


