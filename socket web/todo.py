from models import Model
import time

# 继承自 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        self.created_time = int(form.get('created_time', None) or time.time())
        self.update_time = int(form.get('update_time', None) or self.created_time)
        # 还应该增加 时间 等数据'

    def get_format_time(self):
        '''获取格式化后的时间 返回创建时间和修改时间'''
        ct = time.localtime(self.created_time)
        ut = time.localtime(self.update_time)
        ct = time.strftime('%Y-%m-%d %H:%M:%S', ct)
        ut =time.strftime('%Y-%m-%d %H:%M:%S', ut)
        return ct, ut
