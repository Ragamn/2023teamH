from flask import Flask, render_template,request,redirect,url_for,session
import db,string,random,os,admin_db
from datetime import timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from flask import flash
from flask import request, jsonify
from models import db, Post 
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters,k=256))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/register')
def register():
  return render_template('register.html')

@app.route('/register_exe', methods=['POST'])
def register_exe():
  accountname = request.form.get('accountname')
  mail = request.form.get('mail')
  password = request.form.get('password')
  
  if accountname == '':
    error = 'ユーザ名が未入力です'
    return render_template('register.html', error=error)
  
  if mail == '':
    error = 'メールアドレスが未入力です'
    return render_template('register.html', error=error)
  
  if password == '':
    error = 'パスワードが未入力です'
    return render_template('register.html', error=error)
  
  count = db.register_user(accountname, mail, password)
  
  if count == 1:
    msg = '登録が完了しました。'
    return redirect(url_for('index',msg=msg))
  else:
    error = '登録に失敗しました。'
  return render_template('register.html',error=error)

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/home',methods=['POST'])
def home():
    mail = request.form.get('mail')
    password = request.form.get('password')
  
  # ログイン判定
    if db.user_login(mail, password):
      session['user'] = True # session にキー：'user', バリュー:True を追加
      session.permanent = True # session の有効期限を有効化
      app.permanent_session_lifetime = timedelta(minutes=30)# session の有効期限を5 分に設定
      if mail == 's.kubota.sys22@morijyobi.ac.jp':
        return redirect(url_for('post'))
      else:
        return render_template('post.html')
    else :
        error = 'ログインに失敗しました。'
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {
          'mail':mail,
          'password':password
        }
        return render_template('index.html',error=error,data=input_data)

 
  
# ホームページ - 投稿一覧を表示
@app.route('/homepage')
def home():
    # 削除されていない投稿を取得
    posts = Post.query.filter_by(is_deleted=False).order_by(Post.timestamp.desc()).all()
    return render_template('home.html', posts=posts)
  
# 投稿を削除
@app.route('/delete_post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # 投稿の作者がログインユーザーであるか確認
    if post.author == current_user:
        # 論理削除フラグを立てる
        post.is_deleted = True
        db.session.commit()
        flash('投稿が削除されました', 'success')
    else:
        flash('他のユーザーの投稿は削除できません', 'danger')

    return redirect(url_for('home'))

  
if __name__ == '__main__':
  app.run(debug=True)