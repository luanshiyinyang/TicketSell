# 简单的django实现的购票web项目
- 实现功能
   - 用户的注册，登录
   - 非登录用户和登录用户的车票查询
   - 登录用户的购票，退票
   - 登录用户的已购车票(订单）查询
   - API请求支持
- 使用框架
   - django（python）
   - djangorestframework(python)
   - bootstrap（web）
   - requests(python spider)
- 环境需求
   - linux服务器环境,启用80端口重定向8000
   - python3.x
   - django2.0
   - requests
   - mysql-server,mysql-client
- 服务器admin配置
   - id:admin
   - password:admin123
- 配置步骤
	- 个人服务器root登录（使用linux作为服务端）
	- 按照环境需求安装配置
	- 将项目文件夹放到服务器中（利用putty或者xftp）
	- 切换到该目录下（cd TicketSell)
	- 登录数据库，创建项目需求的数据库(mysql -u root -p,输入密码, create database ticketdata;exit;)
	- 同步服务器中的数据库与项目数据库配置(python manage.py makemigrations, python manage.py migrate)
	- 创建管理员账户(python manage.py createsuperuser, 按照步骤输入)
	- 运行该项目(python manage.py runserver 0.0.0.0:8000)
	- 浏览器输入地址访问该Web服务
### 公网ip
   - 如果懒得部署想要直接看效果，可以访问我的个人服务器地址，此服务器2019年12月之前有效
   - http://54.169.167.51
    
    


