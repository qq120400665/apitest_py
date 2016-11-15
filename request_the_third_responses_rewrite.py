class ApiCall:
	def handle_eachcase(self,file1):
		#对excel每条case处理，只保留参数部分
		caselists = self.excel_tabel_byindex(file1)
		print 'caselists:',json.dumps(caselists, encoding='UTF-8', ensure_ascii=False)
		for caselist in caselists:
			for i in caselist.keys():
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
		caselists_params = caselists
		print 'caselists_params:',json.dumps(caselists_params, encoding='UTF-8', ensure_ascii=False) 
		return caselists_params
	def handle_sign(self,file1,name=None):
		caselists_params = self.handle_eachcase(file1)
		names = names or {}
		eachparam_connect = []
		params = []
		#用=连接各个参数
		for caselists_param in caselists_params:
			if caselists_param != {}:
				for i in caselists_param:
					eachparam = str(i)+'='+str(caselists_param[i])
					eachparam_connect.append(eachparam)
			else:
				eachparam_connect.append(caselists_param)
		#用appid appkey 和参数生成sign
		nonce = 'nonce='+str(time.time()).split('.')[0]+'000'
		for name in names:
			print '=============handle %s' %(name) ,'the %sst case' %n ,'======='
			appid = 'appid='+str(names[name][0])
			appkey = 'appkey='+str(names[name][1])
			eachparam_connect.append(nonce)
			eachparam_connect.append(appid)
			eaeachparam_connect.sort()
			eachparam_connect.append(appkey)
			sign_ex = '&'.join(eachparam_connect)
			sign = hashlib.sha1(sign_ex).hexdigest()
			param_ex = {'appid':names[name][0],'nonce':nonce,'sign':sign}
			param = param_ex.update(param_ex)
			params.append(param)
		print 'params:',json.dumps(params, encoding='UTF-8', ensure_ascii=False) 
		return params








