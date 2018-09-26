from django.apps import AppConfig


class UserOperationConfig(AppConfig):
    name = 'user_operation'
    verbose_name = '用户操作'

    def ready(self):
        # 必须给django信号量配置就绪函数
        import user_operation.signals
