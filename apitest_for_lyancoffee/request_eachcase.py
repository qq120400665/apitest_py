# -*- coding: utf-8 -*-

__author__ = 'Salyu'

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

    def request_eachcase(self):
        #请求接口
        aa = HandleCasesFromExcel('./case_config.ini')
        (case_id,methods,urls,cases,case_description) = aa.handle_caseid()
        results = []
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        #print 'cases:',cases
        for i in range(len(case_id)):
            result = {}
            #print methods[i]
            #print urls[i]
            #print cases[i].values()[0]
            # print 'cases[i]:',cases[i]
            response = self.apicall(methods[i],urls[i],cases[i],headers)
            #print cases[i].keys()[0]
            result[cases[i].keys()[0]] = response
            #print 'result:',json.dumps(result,encoding='UTF-8',ensure_ascii=False)
            results.append(result)
        print 'results:',json.dumps(results,encoding='UTF-8',ensure_ascii=False)
        # for i in results:
        #     print i.keys(),':',json.dumps(i.values(),encoding='UTF-8',ensure_ascii=False)
        return results

if __name__ == '__main__':
	a = ApiCall()
	a.request_eachcase()