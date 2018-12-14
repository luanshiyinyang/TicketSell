'''
created by 周晨
网站路由系统
'''
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views import static
from apps.ticketsale import views
from django.conf import settings
from rest_framework.routers import DefaultRouter

# 创建路由器并注册我们的视图。
router = DefaultRouter()
router.register(r'tickets', views.TicketsViewSet, base_name="tickets")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name='home'),
    path('user_home/', views.index_page_user, name="user_home"),
    path('tickets_search/', views.tickets_search, name="tickets_search"),
    path('ticket_buy/', views.ticket_buy, name="ticket_buy"),
    path('register_after/', views.register_after, name="register_after"),
    path('login_after/', views.login_after, name="login_after"),
    path('order_search/', views.order_search, name="order_search"),
    path('order_cancel', views.order_cancel, name="order_cancel"),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_URL}, name='static'),
    # API路由
    url(r'^api/', include(router.urls))
]
