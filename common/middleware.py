# coding:utf-8

import time
# from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from user.models import User

# 可保存的位置：(缓存，db，文件)
	# 缓存，
		# 通过session(是基于缓存的)，本身具有区分用户的属性
		# session可以保存用户的状态，你存什么进去，session就可以保存什么
	# 数据库db：因为是频繁的请求，保存到数据库不合适，取数据库里面的数据很耗时间
	# 文件，无法分布式运算，如果访问到不同的服务器，不同服务器之间是无法运算的
	# 全局变量，无法分布式运算

# 保存数据类型：list

# 每秒最大请求次数
MAX_REQUEST_PER_SECOND = 2 

class RequestBlockingMiddleware(MiddlewareMixin):
	# 
	def process_request(self,request):
		# 获得当前时间戳
		now = time.time()
		# 取出历史时间队列
		request_queue = request.session.get('request_queue',[])
		# 判断队列长度
		if len(request_queue) < MAX_REQUEST_PER_SECOND:
			# 小于额定队列，放行
			request_queue.append(now)
			request.session['request_queue'] = request_queue
			print('放行')
		else:
			# 达到额定队列长度，检查与最早时间戳的时差
			time0 = request_queue[0]
			if (now - time0) < 1:
				print('waitting-----------int(now)')
				# 请求太频繁，等待1秒
				time.sleep(1)
				print('return-------------int(time.time())')
			request_queue.append(time.time())
			request.session['request_queue'] = request_queue[1:] #截取列表，维持额定列表长度


















