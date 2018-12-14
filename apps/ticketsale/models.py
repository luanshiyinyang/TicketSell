"""
created by 周晨
数据库定义：几个表
数据库：mysql
"""

from django.db import models


# 完成注册的用户信息表
class Users(models.Model):
    # 主键，用手机号唯一标识某个用户，一个用户（也就是一个手机号）能也只能购买一张票
    phone = models.CharField(max_length=15, null=False, verbose_name=u'用户手机号')
    password = models.CharField(default="", max_length=20, null=False, verbose_name="账户密码")
    name = models.CharField(max_length=20, null=True, verbose_name=u'用户姓名')
    createTime = models.DateField(null=False, verbose_name=u'账户创建时间')
    email = models.EmailField(default="", null=False, verbose_name="账户关联邮箱")
    # 车票编号是车票编号的唯一区分，用户获得的是自己的车次+座位号
    ticket_num = models.CharField(max_length=10, null=True, verbose_name=u"购买车票编号")
    ticket_name = models.CharField(max_length=30, null=True, verbose_name=u"购买车票名称")
    ticket_seat_num = models.IntegerField(null=True, verbose_name=u"购买车票座位号")
    ticket_time = models.CharField(null=True, max_length=50, verbose_name=u"购买车票发车时间")

    def __str__(self):
        return self.phone

    # 元数据
    class Meta:
        # 自定义表名，不指定django自动生成
        db_table = 'Users'
        # 可读的名字
        verbose_name = "用户信息"
        # 可读名字的复数形式
        verbose_name_plural = verbose_name


# 每一趟车的车票信息
class Tickets(models.Model):
    # 车次，主键，格式为：类型+编号，eg：G504
    num = models.CharField(default='K100', max_length=210, verbose_name=u"车票编号", null=False)
    name_start = models.CharField(max_length=30, verbose_name=u"始发站", null=False, default="")
    name_end = models.CharField(max_length=30, verbose_name=u"终点站", null=False, default="")
    date = models.CharField(verbose_name=u"车票日期", max_length=50, null=False)
    time = models.CharField(verbose_name=u"车票发车时间", max_length=50, null=False)
    # 车票说明，一些描述，后期放弃该项内容
    brief = models.TextField(max_length=300, verbose_name=u"车票信息", null=True)
    # 剩余座位
    seats = models.IntegerField(default=45, verbose_name=u"剩余座位", null=False)

    def __str__(self):
        return self.num

    class Meta:
        db_table = 'Tickets'
        verbose_name = "车票信息"
        verbose_name_plural = verbose_name

