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
                result = requests.post(url,data=postparams,headers=headers)
            else:
                result = requests.post(url,headers=headers)

        if method == 'PUT':
            if putparams != '':
                result = requests.put(url,params=putparams,headers=headers)
            else:
                result = requests.put(url,headers=headers)
              
        try:
            #jsdata = json.loads(result.text)
            #return jsdata
            #print jsdata
            print result.encoding
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

    def request_the_third(self,file1,names=None):
        '''处理case里的各项参数，并request'''
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
                #input("Prease <enter>")'''
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
                #input("Prease <enter>")'''
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
                #input("Prease <enter>")'''
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
                n = n+1

    def request_the_third_who(self,file,names=None):
        names = names or []
        for name in names:
            result = self.request_the_third(file)
            return result

    def request_the_third_response(self,file1,names=None):
        '''计算不同接口的sign签名并调用接口'''
        response = {}
        names = names or {}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        
        list1 = self.excel_table_byindex(file1)
        
        nonce = str(time.time()).split('.')[0]+'000'
        nonce_ex = 'nonce='+str(time.time()).split('.')[0]+'000'
        n = 1  
        caselist2 = []
        caselist3 = [] 
        for i in list1:
            i = eval(str(i))
            caselist = i 
            method = i['method']
            url = str(i['url'])
            print type(caselist)
            for i in caselist.keys():
                print type(i)
                print 'i:',i
                if caselist[i] == '':
                    caselist.pop(i)
                if i == 'method':
                    caselist.pop(i)
                if i == 'url':
                    caselist.pop(i)
                if i == 'status':
                    caselist.pop(i)
                if i == 'description':
                    caselist.pop(i)
                caselist1 = caselist
                #print 'caselist1:',caselist1
            if caselist1 != {}:
                print 111
                for i in caselist1.keys():
                    eachparam = str(i)+'='+str(caselist1[i])
                    caselist2.append(eachparam)
                    print 222
                    print caselist2
                for name in names:
                    print 444
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    appid = 'appid'+'='+str(names[name][0])
                    appkey = 'appkey' +'='+str(names[name][1])
                    print 333
                    caselist2.append(nonce_ex)
                    caselist2.append(appid)
                    print 'caselist2:',caselist2
                    caselist2.sort()
                    caselist2.append(appkey)
                    print 'caselist2:',caselist2

                    sign_ex = '&'.join(caselist2)
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    params_ex = {'appid':names[name][0],'nonce':nonce,'sign':sign}
                    print 'params_ex:',params_ex
                    #print 'caselist1:',caselist1
                    caselist1.update(params_ex)
                    params = caselist1
                    print 'params:',params
                    if method == 'GET':
                        getparams = params
                        postparams = ''
                        putparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    if method == 'POST':
                        postparams = params
                        getparams = ''
                        putparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    if method =='PUT':
                        putparams = params
                        getparams = ''
                        postparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers) 
                    return response
                    n+=1
                print 555

            else:
                print 2222
                for name in names.keys():
                    print u'========================now running apitest of %s' %(name) ,',the %sst case' %n,'======================'
                    appid = 'appid'+'='+str(names[name][0])
                    appkey = 'appkey' +'='+str(names[name][1])
                    caselist3.append(nonce_ex)
                    caselist3.append(appid)
                    
                    caselist3.sort()
                    caselist3.appen(appkey)
                    sign_ex = '&'.join(caselist3)
                    print sign_ex
                    sign = hashlib.sha1(sign_ex).hexdigest()
                    print sign
                    params_ex = {'appid':names[name][0],'nonce':nonce,'sign':sign}
                    caselist1.update(params_ex)
                    params = caselist1
                    if method == 'GET':
                        getparams = params
                        postparams = ''
                        putparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    if method == 'POST':
                        postparams = params
                        getparams = ''
                        putparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers)
                    if method =='PUT':
                        putparams = params
                        getparams = ''
                        postparams = ''
                        response = self.apicall(method,url,getparams,postparams,putparams,headers)  
                    #return response
                    #n+=1

    def response_compare(self,file1,names=None):
        '''比较status'''
        response = self.request_the_third_response(file1,names)

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
            #continue
                


               

if __name__ =='__main__':
    '''names={'app_qusong':['e2beb30fe93cd5ca9ed0ba705a4e6096','4252855545bfabcf39a7d7d2ea7e268b9925d81e'],
    'app_wokuaidao':['9c838579adda7f729382e226459340e3','7fd154b4fa0afa268f607dde2c381703aa108c21'],
    'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a'],
    'app_sweets':['9fde23f821e48ddb20164374957ef772','36412135402bc7d6821781dcc10e5b25abc1ab00'],
    'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}'''
    api_case = '.\\api_case_the_third_1.xlsx'
    #names={'app_weidian':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
    #names={'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}
    #names={'app_chubao':['77f18b5fbe3979e9f53ffe09b6004ee5','5f373003a793fd123e13de399ab502fc35b3e34a']}
    names = {'app_ali':['dbc1e0a09f15cac4cabf38ed5c0d5974','7e5c0e6a82e026588f4abf02260fa7c3']}
    a = CallApi()
    #if 'courier_barista' in api_case:
        #a.request_courier_barista(api_case)
        #input("Prease <enter>")
    #if 'the_third' in api_case:
        #a.request_the_third(api_case,names)
        #input("Press <enter>")
    if 'the_third' in api_case:
        a.response_compare(api_case,names)
        #a.request_the_third_response(api_case,names)
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


