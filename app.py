from flask import Flask, render_template,request,redirect,url_for,session
import db,string,random,os,admin_db
from datetime import timedelta
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from flask import flash
from flask import request, jsonify
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

#利用者ログイン
@app.route('/home',methods=['POST'])
def home():
    mail = request.form.get('mail')
    password = request.form.get('password')
  
  # ログイン判定
    if db.user_login(mail, password):
      user_id = db.get_user_id(mail)
      session['user'] = True # session にキー：'user', バリュー:True を追加
      session['user_id'] = user_id[0]
      session.permanent = True # session の有効期限を有効化
      app.permanent_session_lifetime = timedelta(minutes=30)# session の有効期限を5 分に設定
      return render_template('post.html')
    else :
        error = 'ログインに失敗しました。'
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {
          'mail':mail,
          'password':password
        }
        return render_template('index.html',error=error,data=input_data)
    
@app.route('/logout')
def logout():
  session.pop('user', None) # session の破棄
  session.pop('user_id', None) # session の破棄
  return redirect(url_for('login')) # ログイン画面にリダイレクト
      
@app.route('/post')
def post():
   return render_template('post.html')

@app.route('/register_post',methods=['POST'])
def register_post():
    if 'user' in session:
      post = request.form.get('post')
      # latitude = request.form['latitude']
      # longitude = request.form['longitude']
      latitude = request.form.get('latitude')
      longitude = request.form.get('longitude')
      file = request.files['file']
      user_id = session['user_id']
      # 都道府県名から県番号を取得するディクショナリを作成
      prefecture_mapping = {
          '北海道': 1,
          '青森県': 2,
          '岩手県': 3,
          '宮城県': 4,
          '秋田県': 5,
          '山形県': 6,
          '福島県': 7,
          '茨城県': 8,
          '栃木県': 9,
          '群馬県': 10,
          '埼玉県': 11,
          '千葉県': 12,
          '東京都': 13,
          '神奈川県': 14,
          '新潟県': 15,
          '富山県': 16,
          '石川県': 17,
          '福井県': 18,
          '山梨県': 19,
          '長野県': 20,
          '岐阜県': 21,
          '静岡県': 22,
          '愛知県': 23,
          '三重県': 24,
          '滋賀県': 25,
          '京都府': 26,
          '大阪府': 27,
          '兵庫県': 28,
          '奈良県': 29,
          '和歌山県': 30,
          '鳥取県': 31,
          '島根県': 32,
          '岡山県': 33,
          '広島県': 34,
          '山口県': 35,
          '徳島県': 36,
          '香川県': 37,
          '愛媛県': 38,
          '高知県': 39,
          '福岡県': 40,
          '佐賀県': 41,
          '長崎県': 42,
          '熊本県': 43,
          '大分県': 44,
          '宮崎県': 45,
          '鹿児島県': 46,
          '沖縄県': 47
      }

      # JSONデータから都道府県名を取得する
      # location_dataには緯度経度空取得したjsonのデータが入っている
      location_data = db. get_location_from_latlng(latitude, longitude)
      print("")
      print("緯度経度")
      print(latitude)
      print(longitude)
      print("中身だった")
      print("")
      print("ここでエラー")
      print(location_data)
      province = location_data.get('address', {}).get('province', '')

      # 県番号を取得する
      prefecture_number = prefecture_mapping.get(province, 0)  # 0はデフォルト値（見つからない場合）
      if file.filename == '':
        db.user_post(user_id,post,prefecture_number)
      else:
        file.save('img/'+file.filename)
        db.user_post_img(user_id,post,prefecture_number,file.filename)
      return render_template('post.html')
    else :
      return redirect(url_for('login'))

#管理者routing
@app.route('/admin')
def admin():
  return render_template('admin_login.html')

#管理者ログイン
@app.route('/management',methods=['POST'])
def management():
    mail = request.form.get('mail')
    password = request.form.get('password')
  
    if admin_db.user_login(mail, password):
      session['admin'] = True # session にキー：'user', バリュー:True を追加
      session.permanent = True # session の有効期限を有効化
      app.permanent_session_lifetime = timedelta(minutes=30)# session の有効期限を5 分に設定
      return render_template('account_management.html')
    else :
        error = 'ログインに失敗しました。'
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {
          'mail':mail,
          'password':password
        }
        return render_template('admin_login.html',error=error,data=input_data)

@app.route('/account_management',methods=['GET'])
def account_management():
  return render_template('account_management.html')

@app.route('/register_advice',methods=['GET'])
def register_advice():
  return render_template('register_advice.html')

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