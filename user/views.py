

# Create your views here.
from django.shortcuts import render,redirect
from user.forms import RegisterForm,LoginForm
from user.helper import permit

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # form.save()方法中传递一个参数commit，赋值为False，代表不要提交到数据库
            user = form.save(commit=False)
            user.save()
            # 设置session
            request.session['uid'] = user.id
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'errors': form.errors})
    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user,passed = form.chk_password()
            if passed:
                request.session['uid'] = user.id
                return redirect('/post/home/')
        else:
            return render(request,'login.html',{'errors':form.errors})
    return render(request,'login.html')

# @permit('user')
def info(request):
    user = getattr(request,'user',None)
    if user is None:
        return redirect('/user/login')
    else:
        return render(request,'info.html',{'user':user})

    return render(request,'info.html')

def logout(request):
    request.session.flush()
    # return render(request,'home.html')
    return redirect('/post/home/')
