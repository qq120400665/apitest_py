# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import json
from handle_cases_fromexcel import HandleCasesFromExcel


class ApiCall():
	#用request模块调用请求方法
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

    def request_eachcase(self,file1,names):
        #请求接口
        aa = HandleCasesFromExcel()
        (methods,urls,case_id,cases) = aa.handle_caseid(file1,names)
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

api_case = 'c:\\Users\\lyancoffee\\Desktop\\apitest\\api_case_the_third.xlsx'
names = [{'app_ali':['dbc1e0a09f15cac4cabf38ed5c0d5974','7e5c0e6a82e026588f4abf02260fa7c3']},{'app_zhuli':['ad5180fff668ac1bc93c368cb6f0a2cb','d563a3e51f3b34d2f02c5159df010db43eaefaa7']}]

if __name__ == '__main__':
	a = ApiCall()
	a.request_eachcase(api_case,names)