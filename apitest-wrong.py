#coding=utf-8
import requests
import json
import os
import time
import xlrd,xlwt

class CallApi():
	u'''调用接口类'''
	
	def apicall(self,method,url,getparams,postparams,putparams,headers):
		result = ''
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		if method == 'GET':
			if getparams != '':
				result = requests.get(url,getparams,headers)
			else:
				result = requests.get(url,headers)

		if method == 'POST':
			if postparams != '':
				result = requests.post(url,postparams,headers)
			else:
				result = requests.post(url,headers)

		if method == 'PUT':
			if putparams != '':
				result = requests.put(url,putparams,headers)
			else:
				result = requests.put(url,headers)

		try:
		  	jsdata = json.loads(result.text)
		  	return jsdata
			#print jsdata
		except Exception,e:
		  	print Exception,':',e
		#print jsdata
		#return jsdata
		

	'''调用测试用例'''
	def excel_data(self,api_case):
		headers = {'content-type': 'application/x-www-form-urlencoded'}
		api_case = r'C:\\Users\\lyancoffee\\Desktop\\apitest\\api_case.xlsx'
		book = xlrd.open_workbook(api_case)
		api_sheet = book.sheet_by_index(0)
		nrows = api_sheet.nrows
		for i in range(1,nrows):
			print '==========NOW RUNNINF APICASE',i,'=============='
			method = api_sheet.cell(i,0).value
			url = api_sheet.cell(i,1).value
			getparams = api_sheet.cell(i,2).value
			if getparams != '':
				getparams = eval(getparams)
			postparams = api_sheet.cell(i,3).value
			if postparams != '':
				postparams = eval(postparams)
			putparams = str(api_sheet.cell(i,4).value)
			#if putparams != '':
			#	putparams = eval(putparams)
			#status = api_sheet.cell(i,5).value

			data = self.apicall(method,url,getparams,postparams,putparams,headers)
			try:
				data['status'] == 0
				print 'pass'
				print data

			except Exception,e:
		  		print Exception,':',e
				print 'fail'
				print 'status:',data
				continue
				

if __name__ =='__main__':
	api_case = 'C:\\Users\\lyancoffee\\Desktop\\apitest\api_case.xlsx'
	a = CallApi()
	a.excel_data(api_case)

