from django.db import models

from django.contrib.auth.hashers import make_password


class User(models.Model):
	nickname = models.CharField(max_length=32,unique=True,null=False,blank=False)
	password = models.CharField(max_length=32,null=False,blank=False)
	# email = models.EmailField(max_length=254)
	# 头像，使用ImageField需要安装pip install PILLOW
	avarta = models.ImageField(max_length=200)
	age = models.IntegerField()
	sex= models.IntegerField()
	# 权限ID
	pid = models.IntegerField(default=1)

	def save(self):
		if not self.password.startswith('pbkdf2_'):
			self.password = make_password(self.password)
		# 重写save方法
		super().save()

	@property
	def permission(self):
		return Permission.objects.get(self.pid)

# 权限管理：一个权限对应多个user
class Permission(models.Model):
	perm = models.IntegerField()
	name = models.CharField(max_length=64,unique=True)



