from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '用户管理'

    def ready(self):
        # 必须给django信号量配置就绪函数
        import users.signals