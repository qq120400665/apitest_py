# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from request_eachcase import ApiCall
import unittest

class ResponseAssert(unittest.TestCase):

	def setUp(self,test_result=None,fail_reason=None):
		self.test_result = test_result
		self.fail_reason = fail_reason

	def test_compare(self):
		a = ApiCall()
		result = a.request_eachcase()
		for i in result:
			print eval(i.values()[0],globals)['status'] #Python使用eval强制转换字符串为字典时报错：File "<string>", line 1, in <module> NameError: name 'true' is not defined
			try:
				self.assertEqual(eval(i.values()[0],globals)['status'], 0, msg='返回status不等于0')
			except AssertionError as e:
				print('%s' % e)
				self.test_result = 'Fail'
				self.fail_reason = '%s' % e

globals = {'true': 0}
if __name__ =='__main__':
	unittest.main()