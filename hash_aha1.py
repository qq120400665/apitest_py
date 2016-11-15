import hashlib
import time
def hash_sha1():
	
	appid = 'appid=ad5180fff668ac1bc93c368cb6f0a2cb'
	geo = 'geo=121.404147,31.168728'
	nonce = 'nonce='+str(time.time()).split('.')[0]+'000'
	appkey = 'appkey=d563a3e51f3b34d2f02c5159df010db43eaefaa7'
	sign_ex = appid + '&' +geo+'&'+ nonce +'&' + appkey
	sign = hashlib.sha1(sign_ex).hexdigest()
	print nonce
	print sign_ex
	print sign
	#return (nonce,sign)

if __name__ == '__main__':
	hash_sha1()
a="appid=ad5180fff668ac1bc93c368cb6f0a2cb&data={'recipient_name':'张三','recipient_phone':'13564252825','city':'上海','building':'徐汇区古美路1515号', 'room':'1801','buyer_name':'李四','buyer_phone':'13564347512','provider_id':1,'expected_time_id':12,'carts':[{'id':1,'quantity':1}]}&nonce=1448348600000&appkey=d563a3e51f3b34d2f02c5159df010db43eaefaa7"
a='appid=ad5180fff668ac1bc93c368cb6f0a2cb&data={"recipient_name":"宁-T","recipient_phone":"13701230123","city":"上海","building":"北京市东城区中国青年出版社","room":"","buyer_name":"Laiye-T","buyer_phone":13803210321,"provider_id":1,"expected_time_id":14,"remark":"","carts":[{"id":1,"quantity":1}]}&nonce=1448351693000&appkey=d563a3e51f3b34d2f02c5159df010db43eaefaa7'
a='appid=ad5180fff668ac1bc93c368cb6f0a2cb&data={"recipient_name":"宁-T","recipient_phone":"13701230123","city":"上海","building":"北京市东城区中国青年出版社","room":"","buyer_name":"Laiye-T","buyer_phone":13803210321,"provider_id":1,"expected_time_id":14,"remark":"","carts":[{"id":1,"quantity":1}]}&nonce=1448352715000&appkey=d563a3e51f3b34d2f02c5159df010db43eaefaa7'
a = 'appid=ad5180fff668ac1bc93c368cb6f0a2cb&data={"recipient_name":"宁-T","recipient_phone":"13701230123","city":"上海","building":"北京市东城区中国青年出版社","room":"","buyer_name":"Laiye-T","buyer_phone":"13803210321","provider_id":1,"expected_time_id":14,"remark":"","carts":[{"id":1,"quantity":1}]}&nonce=1448353751000&appkey=d563a3e51f3b34d2f02c5159df010db43eaefaa7'