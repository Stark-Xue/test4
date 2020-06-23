from django.shortcuts import render, HttpResponse, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.utils.safestring import mark_safe
from utils import paginations, pagination

# Create your views here.

# def index(request):
#     # 视图获取用户请求相关信息以及请求头 

#     print(type(request))

#     # 封装了所有用户的请求信息
#     print(request.environ)

#     for k,v in request.environ.items():
#         print(k,v)
#     print(request.environ['HTTP_USER_AGENT'])
#     # request.POST
#     # request.GET
#     # request.COOKIES
#     return HttpResponse("ok")

def tpl1(request):
    user_list = [1,2,3,4]
    return render(request, "tpl1.html", {"u": user_list})

def tpl2(request):
    name = "root"
    return render(request, "tpl2.html", {'name': name})

def tpl3(request):
    status = "已删除"
    return render(request, "tpl3.html", {'status': status})

def tpl4(request): # 自定义simple_tag,filter
    name = "asdf"
    return render(request, 'tpl4.html', {"name": name})

LIST = []
for i in range(199):
    LIST.append(i)

def user_list(request):
    print(LIST)
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    print(current_page, type(current_page))
    per_page_count = 10
    xsys = 5
    val = request.COOKIES.get("per_page_count")
    print(val)
    if isinstance(val, int):
        val = int(val)
    else:
        val = per_page_count

    #start = (current_page-1)*per_page_count
    #end = current_page*per_page_count
    page_obj = paginations.Page(current_page, len(LIST), val)
    data = LIST[page_obj.start(): page_obj.end()]
    page_msg = page_obj.page_str('/user_list/')
    return render(request, 'user_list.html', {'user_list': data, 'page_msg': page_msg})




def usr_list(request):
    all_count = len(LIST)
    current_page = int(request.GET.get('p', 1))
    per_page_count = request.COOKIES.get('per_page_count')
    print(per_page_count, type(per_page_count))

    page_obj = pagination.Page(current_page, all_count)

    data = LIST[int(page_obj.start): int(page_obj.end)]

    return render(request, "usr_list.html", {'data': data, 'page_str': page_obj.page_str()})

########## cookie ##########
user_info = {
    'zs': {'p': '123'},
}


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('pwd')
        print("login", u)
        dic = user_info.get(u)
        if not dic:
            return render(request, 'login.html')
        elif dic['p'] == p:
            res = redirect('/index/')
            res.set_cookie('username111', u, max_age=10)
            return res
        else:
            return render(request, 'login.html')

def auth(func): # FBV装饰器
    def inner(request, *args, **kwargs):
        username = request.COOKIES.get("username111")
        print("index", username)
        if not username:
            return render(request, 'login.html')
        return func(request, *args, **kwargs)
    return inner


@auth
def index(request):
    username = request.COOKIES.get("username111")
    # #username = request.COOKIES['username111']
    # print("index", username)
    # if not username:
    #     return render(request, 'login.html')
    return render(request, 'index.html', {"username": username})

from django import views
from django.utils.decorators import method_decorator

@method_decorator(auth, name='dispatch') # 和下面的dispatch函数一样的功能
class Order(views.View): # CBV装饰器
    """
    @method_decorator(auth) # 装饰内部所有函数
    def dispatch(self, request, *args, **kwargs):
        return super(Order, self).dispatch(request, *args, **kwargs) """

    # @method_decorator(auth) # 装饰这一个函数
    def get(self, request):
        username = request.COOKIES.get("username111")
        return render(request, 'index.html', {"username": username})
    def post(self, request):
        username = request.COOKIES.get("username111")
        return render(request, 'index.html', {"username": username})

def cookie(request):
    request.COOKIES
    request.COOKIES['username111']
    request.COOKIES.get('username111')

    response = render(request, 'index.html')
    response = redirect('/index/')

    # 设置cookie，关闭浏览器失效
    response.set_cookie("key", 'value')

    # 设置cookie，N秒之后失效
    response.set_cookie("key", 'value', max_age=10)
    
    # 设置cookie，截止时间失效
    import datetime
    current_time = datetime.datetime.utcnow()
    current_time = current_time + datetime.timedelta(seconds=10)
    response.set_cookie('key', 'value', expires=current_time)

    # 带签名的cookie
    obj = HttpResponse('ok')
    obj.set_signed_cookie('username', 'kangbazi', salt='asdfasdf') # 加密
    request.get_signed_cookie('username', salt="asdfasdf") # 解密
    
    return response