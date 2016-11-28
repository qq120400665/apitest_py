# -*- coding: utf-8

__author__ = 'Salyu'

from request_eachcase import ApiCall
from handle_cases_fromexcel import HandleCasesFromExcel
import configparser
import json

class ResponseAssert():

	def __init__(self,initfile):
		self.test_result = []
		self.fail_reason = []
		config = configparser.ConfigParser()
		config.read(initfile)
		self.names = config.get('NAMES','names')

	def compare(self):

		a = ApiCall()
		result = a.request_eachcase()
		for i in result:
			# print eval(i.values()[0],globals)['status'] #Python使用eval强制转换字符串为字典时报错：File "<string>", line 1, in <module> NameError: name 'true' is not defined
			if eval(i.values()[0],globals)['status'] == 0:
				# self.assertEqual(eval(i.values()[0],globals)['status'], 0, msg='status不等于0')
				self.test_result.append('Pass')
				self.fail_reason.append('')
			else:
				# print('%s' % e)
				self.test_result.append('Fail')
				self.fail_reason.append(i.values())

		print self.test_result
		return self.test_result,self.fail_reason

	def handle_for_report(self):
		#拼装report所需格式
		caseid_list = []
		case_id = []
		test_result = []
		test_reason = []
		data_report = []
		a = HandleCasesFromExcel('./case_config.ini')
		(caseid,method,urls,cases,case_description) = a.handle_caseid()
		#print 'caseid:',list(set(caseid))
		for i in caseid:
			if i not in case_id:
				case_id.append(i)
		for i in case_id:   #列表去重
			for j in eval(self.names):
				print 'j:',j
				caseid_list.append(str(j).split(':')[0][1:]+'_'+i)
		(test_result,test_reason) = self.compare()
		test_result_pass = test_result.count('Pass')
		test_result_fail = test_result.count('Fail')
		test_result_total = len(test_result)
		data_report = zip(caseid_list,case_description,method,urls,cases,test_result,test_reason)
		print 'data_report:',json.dumps(data_report,encoding='UTF-8',ensure_ascii=False)
		return data_report,test_result_pass,test_result_fail,test_result_total

globals = {'true': 0,'false':-1}
if __name__ =='__main__':
	aa = ResponseAssert('./case_config.ini')
	aa.handle_for_report()
