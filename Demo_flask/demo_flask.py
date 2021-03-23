from flask import Flask

# 构造函数的 name 参数传给Flask程序，便于找到根目录以及资源文件
app = Flask(__name__)


# 装饰器
@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>' % name


if __name__ == '__main__':
    # 启动flask框架，开启debug调试模式
    app.run(debug=True)
