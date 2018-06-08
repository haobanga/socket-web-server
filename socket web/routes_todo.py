from utils import log, template_render, http_response, redirect
from todo import Todo
from models import User
import time
from session import current_user


def login_required(func):
    def warp(request):
        username = current_user(request)
        if username is None:
            return redirect('/login')
        user = User.find_by(username=username)
        return func(request, user)
    return warp
    
    
@login_required
def admin_index(request, u):
    # 认证石否为管理员
    if u.role != 1:
        log('admin not power', u.role)
        return redirect('/login')
    log('admin', u)
    users = User.all()
    return http_response(template_render('admin_index.html', users=users))


@login_required
def user_update(request, u):
    # 认证石否为管理员
    if u.role != 1:
        log('admin not power', u)
        return redirect('/login')
    if request.method == 'POST':
        # 修改并且保存 todo
        form = request.form()
        #print('debug update', form)
        user_id = form.get('id', -1)
        password = form.get('password', '')
        # 检查 输入是否合法
        if password == '' or user_id == -1 or not user_id.isdigit():
            log('form error', form)
            return redirect('/admin/user')
        user_id = int(user_id)
        user = User.find_by(id=user_id)
        # 检查要修改的用户是否存在
        if user is None:
            log('user update', 'user not exist')
            return redirect('/admin/user')
        log('user update', user, 'admin', u)
        user.update_password(password)
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/admin/user')



@login_required
def index(request, u):
    """
    todo 首页的路由函数
    """
    
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    todos = Todo.find_all(user_id=u.id)
    # 下面这行生成一个 html 字符串
    # todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
    #                      for t in todo_list])
    # 上面一行列表推倒的代码相当于下面几行
    return http_response(template_render('todo_index.html',todos=todos))


@login_required
def edit(request, u):
    """
    todo edit 的路由函数
    """

    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = request.query.get('id', -1)
    # 检查 id 是不是数字
    if todo_id == -1 or not todo_id.isdigit():
        return redirect('/todo')
    todo_id = int(todo_id)
    todo = Todo.find_by(id=todo_id)
    if todo is None or todo.user_id != u.id:
        return redirect('/todo')
    # if todo_id < 1:
    #     return error(404)
    # 替换模板文件中的标记字符串 header = response_with_headers(headers)

    return http_response(template_render('todo_edit.html',todo=todo))


@login_required
def add(request, u):
    """
    用于增加新 todo 的路由函数
    """
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    if request.method == 'POST':
        # 'title=aaa'
        # {'title': 'aaa'}
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


@login_required
def update(request, u):
    """
    用于增加新 todo 的路由函数
    """
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    if request.method == 'POST':
        # 修改并且保存 todo
        form = request.form()
        #print('debug update', form)
        todo_id = form.get('id', -1)
        # 检查 id 是不是数字
        if todo_id == -1 or not todo_id.isdigit():
            return redirect('/todo')
        todo_id = int(todo_id)
        t = Todo.find_by(id=todo_id)
        # 检验用户权限
        if t is None or t.user_id != u.id:
            return redirect('/todo')
        t.title = form.get('title', t.title)
        t.update_time = int(time.time())
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


@login_required
def delete_todo(request, u):
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = request.query.get('id', -1)
    # 检查 id 是不是数字
    if todo_id == -1 or not todo_id.isdigit():
        return redirect('/todo')
    todo_id = int(todo_id)
    t = Todo.find_by(id=todo_id)
    # 检验用户权限
    if t is None or t.user_id != u.id:
        return redirect('/todo')
    t.remove()
    return redirect('/todo')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求, 处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete_todo,
    '/admin/user': admin_index,
    '/admin/user/update': user_update
}
