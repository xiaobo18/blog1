
from django.shortcuts import render
from user.models import Permission


def check_permission(user,perm_name):
	# 检查用户是否具有该权限
	# 下面是两个Permission对象
	# 用户权限
	user_perm = Permission.objects.get(id=user.pid)
	# 需要的权限，perm_name是装饰器的参数
	need_perm = Permission.objects.get(name=perm_name)
	# 返回值：用户权限>=需要的权限就可以进行操作
	return user_perm.perm >= need_perm.perm



def permit(perm_name):
	# 权限检查装饰器
    def wrap1(view_func):
        def wrap2(request,*args,**kwargs):
        	# 因为先进行中间件的操作，所以可以从request.user中获取user
            user = getattr(request,'user',None)

            if user is not None:
                if check_permission(user,perm_name):
	                response = view_func(request,*args,**kwargs)
	                return response
            return render(request,'blockers.html')


        return wrap2
    return wrap1





