"""
created by 周晨
视图逻辑处理部分
核心代码
"""
from django.shortcuts import render
from apps.ticketsale.models import Tickets, Users
from apps.ticketsale.forms import UserLoginForm, UserRegisterForm, TicketSearchForm
from apps.ticketsale.serializers import TicketsSerializer
from django.http import HttpResponse, Http404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from utils.spider_12306 import get_query_list
from Assignment.settings import STATICFILES_DIRS
import datetime


def database_update():
    with open(STATICFILES_DIRS[0]+"/update.log", 'r', encoding='utf-8 ') as f:
        last_update = f.read()
    # 判断上次更新的时间和点击主页当天的时间差,三天更新一次数据
    today = datetime.datetime.now().date()
    temp = datetime.timedelta(days=1)
    if (datetime.datetime.now() - datetime.datetime(int(last_update.split("-")[0]), int(last_update.split("-")[1]), int(last_update.split("-")[2]))).days > 3:
        with open(STATICFILES_DIRS[0] + "/update.log", 'w', encoding='utf-8 ') as f:
            f.write(str(today))
        get_query_list(str(today))
        get_query_list(str(today+temp))
        get_query_list(str(today+temp+temp))
        with open(STATICFILES_DIRS[0]+"/"+str(today)+".txt", 'r', encoding='utf-8') as f:
            temp = f.readline()
            while temp:
                temp = temp.split()
                try:
                    Tickets.objects.create(num=temp[4], name_start=temp[0], name_end=temp[1], time=str(today)+" " + temp[2], seats=45)
                    print("数据库更新")
                except:
                    pass
                temp = f.readline()
    else:
        pass


def init_index_data():
    '''
    用于form与数据库交互
    :return:
    '''

    date_set = list()
    import datetime
    for i in range(0, 7):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        now_year = date.year
        now_month = date.month
        now_day = date.day
        now_date = str(now_year) + "-" + str(now_month) + "-" + str(now_day)
        date_set.append((now_date, now_date))
    return date_set


# 未登录的主页
def index_page(request):
    database_update()
    date_set = init_index_data()
    # 用户注册表单
    user_login_form = UserLoginForm()
    user_register_form = UserRegisterForm()
    ticket_search_form = TicketSearchForm()
    ticket_search_form.fields["date_start"].choices = date_set
    tickets = Tickets.objects.all()
    # 打包dict
    context = {
        'user_login_form': user_login_form,
        'user_register_form': user_register_form,
        'ticket_search_form': ticket_search_form,
        'tickets': tickets,
    }
    rsp = render(request, 'index.html', context=context)
    # 每次只要回到了无用户状态的主页，如果存在cookie项则删除
    try:
        rsp.delete_cookie("username")
    except Exception as e:
        pass
    return rsp


# 登录后的主页
def index_page_user(request):
    date_set = init_index_data()
    try:
        name = request.COOKIES["username"]
    except Exception as e:
        name = None
    if name == None:
        return index_page(request)
    else:
        ticket_search_form = TicketSearchForm()
        ticket_search_form.fields["date_start"].choices = date_set
        tickets = Tickets.objects.all()
        content = {
                'user_name': name,
                'ticket_search_form': ticket_search_form,
                'tickets': tickets,
            }
        rsp = render(request, 'userhome.html', context=content)
    return rsp


def register_after(request):
    user_form = UserRegisterForm(request.POST)
    if user_form.is_valid():
        if request.method == 'POST':
            register_phone = request.POST['phone']
            if request.POST['password'] == request.POST['again_password']:
                register_password = request.POST['password']
            else:
                rs_str = r'注册失败！密码不一致'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
            register_email = request.POST['email']
            try:
                result = Users.objects.get(phone=register_phone)
            except Exception as e:
                result = None
            # 查询不到该用户，可以注册
            if result is None:
                import datetime
                date = str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day)
                Users.objects.create(phone=register_phone, password=register_password, email=register_email, createTime=date)
                rs_str = r'注册成功！'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
            else:
                rs_str = r'用户存在！'
                content = {
                    "string": rs_str
                }
                return render(request, 'register_after.html', context=content)
        else:
            rs_str = r'提交错误，存在不合法数据！'
            content = {
                "string": rs_str
            }
            return render(request, 'register_after.html', context=content)
    else:
        rs_str = r'提交错误，存在不合法数据！'
        content = {
            "string": rs_str
        }
        return render(request, 'register_after.html', context=content)


def login_after(request):
    user_form = UserLoginForm(request.POST)
    if user_form.is_valid():
        if request.method == 'POST':
            login_phone = request.POST['phone']
            password = request.POST['password']
            try:
                result = Users.objects.get(phone=login_phone, password=password)
            except Exception as e:
                result = None
            # 查询不到该用户，表示没有在数据库中
            if result is None:
                rs_str = r'登录失败，用户名或者密码错误！'
                content = {
                    "string": rs_str,
                    "name": "",
                }
                return render(request, 'register_after.html', context=content)
            else:
                rs_str = r'登录成功！'
                content = {
                    "string": rs_str,
                    "name": login_phone,
                }
                rsp = render(request, 'login_after.html', context=content)
                rsp.set_cookie("username", login_phone)
                return rsp
        else:
            rs_str = r'提交错误，存在不合法数据！'
            content = {
                "string": rs_str,
                "name": ""
            }
            return render(request, 'register_after.html', context=content)
    else:
        rs_str = r'提交错误，存在不合法数据！'
        content = {
            "string": rs_str
        }
        return render(request, 'register_after.html', context=content)


def tickets_search(request):
    if request.method == 'POST':
        tickets = Tickets.objects.filter(name_start=request.POST["name_start"], name_end=request.POST["name_end"],
                                         date=request.POST["date_start"])
        ticket_list = []
        for item in tickets:
            tic = {"num": item.num, "name": item.name_start + "-" + item.name_end, "date_start": item.time,
                   "seats": item.seats}
            ticket_list.append(tic)
        content = {
            "tickets": ticket_list,
            "user_phone": "",
        }
        rsp = render(request, "tickets_search.html", context=content)
        return rsp

    else:
        # 只要是个正常人，只要使用了submit按钮就不会到这个页面
        return HttpResponse("不合法查询")


def ticket_buy(request):
    flag = True
    try:
        username = request.COOKIES["username"]
    except Exception as e:
        flag = False
    # 没有登录是不可以购票的
    if flag is False:
        content = {
            'result': '非登录用户不能购票,点击按钮回到主页登录或者回到查询界面 '
        }
        rsp = render(request, 'buy_after.html', context=content)
        return rsp
    # 用户登录了
    else:
        if request.method == 'GET':
            ticket_number = request.GET.get("number")
        user = Users.objects.filter(phone=username)
        # 用户想要购票，在得到用户的id之后首先确认是否已经购票（因为一个人只能买一张票）
        # 没有买过票的情况，这时判断该车次有没有票
        if user[0].ticket_num is None or user[0].ticket_num == "":
            ticket = Tickets.objects.filter(num=ticket_number)
            # 该车次还有座位
            if ticket[0].seats > 0:
                user_seat = 45 - ticket[0].seats + 1
                # 更新用户表
                Users.objects.filter(phone=username).update(ticket_num=ticket[0].num,
                                                            ticket_name=ticket[0].name_start+"-"+ticket[0].name_end,
                                                            ticket_seat_num=user_seat,
                                                            ticket_time=ticket[0].date+" "+ticket[0].time)
                Tickets.objects.filter(num=ticket_number).update(seats=ticket[0].seats-1)
                content = {
                    'result': '购票成功,车次为{}'.format(ticket_number)
                }
                rsp = render(request, 'buy_after_logining.html', context=content)
                return rsp
            # 该车次座位余量为0
            else:
                content = {
                    'result': '购票失败，该车次{}已经没有空余座位了'.format(ticket_number)
                }
                rsp = render(request, 'buy_after_logining.html', context=content)
                return rsp
        # 买过票的情况,那么购票一定是失败的
        else:
            content = {
                'result': '购票失败，你已经买票了'
            }
            rsp = render(request, 'buy_after_logining.html', context=content)
            return rsp


def order_search(request):
    try:
        username = request.COOKIES["username"]
    # 一般不会有这个异常，因为只有登录用户能看到订单入口
    except:
        username = None
    if username is None:
        pass
    # 用户登录了
    else:
        user = Users.objects.filter(phone=username)
        # 用户没有买票
        if user[0].ticket_num is None or user[0].ticket_num == "":
            content = {
                'result': '未购票',
                'userinfo': user[0]
            }
        else:
            content = {
                'result': '已经购票',
                'userinfo': user[0]
            }
        rsp = render(request, 'order_search.html', context=content)
        return rsp


def order_cancel(request):
    try:
        username = request.COOKIES["username"]
    except:
        username = None
    if username is None:
        raise Http404
        return HttpResponse()
    else:
        user = Users.objects.filter(phone=username)[0]
        if user.ticket_num is None or user.ticket_num == "":
            content = {
                'string': "取消失败，您未订票"
            }
        else:
            now_seats = Tickets.objects.filter(num=user.ticket_num)[0].seats + 1
            Tickets.objects.filter(num=user.ticket_num).update(seats=now_seats)
            Users.objects.filter(phone=username).update(ticket_num=None, ticket_name=None, ticket_seat_num=None,
                                                        ticket_time=None)
            content = {
                'string': "退票成功"
            }
        return render(request, 'cancel_after.html', context=content)


class TicketsViewSet(viewsets.ModelViewSet):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    @detail_route(renderer_classes=[renderers.JSONRenderer])
    def highlight(self, request, *args, **kwargs):
        ticket = self.get_object()
        return Response(ticket.highlighted)










