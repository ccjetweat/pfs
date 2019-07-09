import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/feedback/')
def feedback():
    try:
        # 创建数据库连接
        conn = sqlite3.connect(r'.\db\feedback.db')
        # 创建游标
        cursor = conn.cursor()
        # 从数据库查询数据
        sql = "SELECT ROWID,CategoryName FROM category"
        # 获取数据库查询的数据
        categories = cursor.execute(sql).fetchall()
    except:
        categories = [(1, "产品质量"), (2, "客户服务"), (3, "购买支付")]
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

    return render_template('post.html', categories=categories)

@app.route('/post_feedback/', methods=['POST'])
def post_feedback():
    # 如果当前请求为POST请求
    if request.method == "POST":
        # 获取表单数据
        subject = request.form.get('subject')
        categoryid = request.form.get('category', 1)
        username = request.form.get('username')
        eamil = request.form.get('email')
        image = request.form.get('image')
        body = request.form.get('body')
        reply = ""
        state = 0
        release_time = datetime.now()

        try:
            # 创建数据库连接和游标
            conn = sqlite3.connect(r".\db\feedback.db")
            cursor = conn.cursor()
            # 插入数据,这种方式可以防止sql注入
            sql = r"insert into feedback values (?,?,?,?,?,?,?,?,?)"
            cursor.execute(sql, (subject, categoryid, username, eamil, image, body, reply, state, release_time))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
            return redirect(url_for('feedback'))

@app.route('/admin/list/')
def feedback_list():

    return render_template('feedback_list.html')

if __name__ == '__main__':
    app.run(debug=True)
