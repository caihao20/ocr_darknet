创建 Django 工程
1.执行命令: django-admin startproject ocr
2.命令执行完成后的目录文件说明：
    manage.py:命令行工具，可以让你通过命令行与该Django交互。比如数据库操作
    ocr_service/init.py:一个空文件，告诉 Python 该目录是一个 Python 包。不常使用但是是必须的
    ocr_service/settings.py: 该 Django 项目的设置/配置。经常使用
    ocr_service/urls.py: 该项目的URL声明; 由 Django 驱动的网站"目录"。可以看做是后台api接口
    ocr_service/wsgi.py: 一个 WSGI 兼容的 Web 服务器的入口，以便运行你的项目。

3.新建一个app



