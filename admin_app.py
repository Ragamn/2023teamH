from flask import Flask, render_template, request, redirect, url_for, session
import db,string,random,admin_db
from datetime import timedelta

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')

    if msg == None:
        return render_template('admin_login')
    else :
        return render_template('admin_login', msg=msg)

# 管理者ログイン機能
@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_mail = request.form.get('admin_mail')
    password = request.form.get('admin_pass')

    # ログイン判定
    if admin_db.login(admin_mail, password):
        session['user'] = True
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=1)
        return redirect(url_for('management.html'))
    else :
        error = 'メールアドレスまたはパスワードが違います。'
        input_data = {'admin_mail':admin_mail, 'admin_pass':password}
        return render_template('admin_login.html', error=error, data=input_data)
    
# ユーザ一覧
@app.route('/user_list')
def user_list():
    user_list = admin_db.get_users()
    return render_template('user_list.html', users=user_list)

# ユーザ削除
@app.route('/user_delete')
def user_delete():
    user_name = request.args.get('user_name')
    admin_db.user_delete(user_name)
    return redirect(url_for('user_list'))

if __name__ == '__main__':
    app.run(debug=True)