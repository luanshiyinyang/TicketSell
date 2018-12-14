"""
created by 周晨
订票系统-表单处理部分
"""

from django import forms
from django.forms import widgets


# 预订车票填写信息Form
class TicketForm(forms.Form):

    name = forms.CharField(label='name', max_length=10, error_messages={'required': '请填写您的姓名',
                                                                        'max_length': '名字太长了'})
    phone_number = forms.CharField(label='phone_number', min_length=11, max_length=11,
                                   error_messages={'required': '手机号码输入不正确',
                                                    'min_length': '您输入的号码数不符合11位',
                                                    'max_length': '您输入的号码数不符合11位'})
    ticket_num = forms.CharField(label='ticket_num', max_length=10, error_messages={'required': '车票编号输入不正确'})


class UserLoginForm(forms.Form):
    phone = forms.CharField(label='phone_number', min_length=11, max_length=11,
                            error_messages={'required': '手机号码输入不正确',
                                            'min_length': '您输入的号码数不符合11位',
                                            'max_length': '您输入的号码数不符合11位'},
                            widget=widgets.TextInput(attrs={"class": "login_register_class", 'placeholder': '输入手机号'}))
    password = forms.CharField(label='password', min_length=8, max_length=20,
                                error_messages={'required': '输入密码',
                                'min_length': '密码不得少于8位',
                                'max_length': '密码不得多于20位'},
                               widget=widgets.TextInput(attrs={"class": "login_register_class", 'placeholder': '输入密码',
                                                               'type': 'password'}))


class UserRegisterForm(forms.Form):
     phone = forms.CharField(label='phone_number', min_length=11, max_length=11,
                             error_messages={'required': '手机号码输入不正确',
                                            'min_length': '您输入的号码数不符合11位',
                                            'max_length': '您输入的号码数不符合11位'},
                             widget=widgets.TextInput(attrs={'class': 'login_register_class', 'placeholder': '输入11位手机号'}))
     password = forms.CharField(label='password', min_length=8, max_length=20,
                                error_messages={'required': '输入密码',
                                                'min_length': '密码不得少于8位',
                                                'max_length': '密码不得多于20位'},
                                widget=widgets.TextInput(attrs={'class': 'login_register_class', 'placeholder': '至少8位密码数字组合',
                                                                'type': "password"}))
     again_password = forms.CharField(label='password', min_length=8, max_length=20,
                                error_messages={'required': '输入密码',
                                                'min_length': '密码不得少于8位',
                                                'max_length': '密码不得多于20位'},
                                widget=widgets.TextInput(attrs={'class': 'login_register_class', 'placeholder': '至少8位密码数字组合',
                                                                "type": "password"}))
     email = forms.EmailField(label='email', error_messages={'required': '输入标准邮箱格式'},
                              widget=widgets.TextInput(attrs={'class': 'login_register_class', 'placeholder': '例如zhouchen@163.com' }))


class TicketSearchForm(forms.Form):
    date_start = forms.ChoiceField(label='date_start', widget=widgets.Select(attrs={"class": "form-control"}))



