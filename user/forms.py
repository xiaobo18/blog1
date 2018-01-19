
from django.forms import Form,ModelForm,CharField
from user.models import User
from django.contrib.auth.hashers import check_password

class RegisterForm(ModelForm):
	class Meta:
		model = User
		fields = ['nickname','password','age','sex']


class LoginForm(Form):
	nickname = CharField(max_length=64)
	password = CharField(max_length=64)

	def chk_password(self):
		# 具有有效数据的表单实例有个 cleaned_data 属性，它的值是一个字典，存储着“清理后的”提交数据
		nickname = self.cleaned_data['nickname']
		password = self.cleaned_data['password']

		try:
			user = User.objects.get(nickname=nickname)
			return user,check_password(password,user.password)
		except:
			return None,False
