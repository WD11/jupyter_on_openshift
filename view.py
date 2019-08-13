from flask import Blueprint, render_template, redirect,request,url_for
from model.Sql_data import get_userdata
USER = {
    1: {'name': 'wdc', 'age': 18, 'text': '我的名字叫做王德昌'},
    2: {'name': 'wdw', 'age': 16, 'text': '我的名字叫做王德武'},
    3: {'name': 'pjj', 'age': 19, 'text': '我的名字叫做潘军军'}
}

main = Blueprint('main',__name__)
# 用来查看是否有用户登录，用session这个全局变量来保存
session = {}
@main.route('/', methods=['GET', 'POST'])  # 每一次将主页设置为‘/’，要修改请求方式，因为在/login的url中要输入东西
def pod_user():
    print ('i\'in pod_user function')
    return redirect(url_for('main.l1'))
@main.route('/login', methods=['GET', 'POST'], endpoint='l1')  # endpoint是一个反向输出
def login():
    if request.method == 'GET':
        print('i\'in get login ')
        return render_template('login.html')
    else:
        print('i\'in post login ')
        user = request.form.get('user')
        pwd = request.form.get('pwd')
        print(user,pwd)
        if_has_user=len(get_userdata(user,pwd))
        if  if_has_user >0:
            # 登录成功后用session来保存这个用户信息
            session['user_info'] = user
            return redirect(url_for('main.router_address', user_name=user))
        return render_template('login.html', error="用户名或密码错误")


@main.route('/index', methods=['GET'])
def index():
    url_1 = url_for('main.l1')
    user = session.get('user_info')
    if user:
        return render_template('index.html', user_dict=USER)
    return redirect(url_1)


@main.route('/detail/<int:nid>', methods=['GET'])
def detail(nid):
    url_1 = url_for('main.l1')
    user = session.get('user_info')
    if user:
        info = USER.get(nid)
        return render_template('detail.html', info=info)
    return redirect(url_1)

@main.route('/router_address/<string:user_name>', methods=['GET'])
def router_address(user_name):
    url_1 = url_for('main.l1')
    user = session.get('user_info')
    if user_name:
        return redirect('http://minimal-notebook-s2i-assigned-uid-{0}-myproject.192.168.99.100.nip.io'.format(user_name))
    return redirect(url_1)