from flask import Flask, render_template,request,redirect,url_for,session,jsonify
import db,string,random,os,admin_db,advice_emotion_db
from datetime import timedelta
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
import matplotlib.font_manager
matplotlib.use('Agg')

# 使用するフォントを設定
font_path = "C:\\Windows\\Fonts\\meiryo.ttc"  # フォントファイルのパス
plt.rcParams['font.family'] = matplotlib.font_manager.FontProperties(fname=font_path).get_name()
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
      if db.get_flg(mail):
        user_id = db.get_user_id(mail)
        session['user'] = True # session にキー：'user', バリュー:True を追加
        session['user_id'] = user_id[0]
        session.permanent = True # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=30)# session の有効期限を5 分に設定
        post_list = db.get_all_post()
        return render_template('post.html',post_list = post_list,name="/static/img/",user_id=session['user_id'])
      else:
         error = 'アカウントが削除されています'
         input_data = {
          'mail':mail,
          'password':password
        }
         return render_template('login.html',error=error,data=input_data)
    else :
        error = 'ログインに失敗しました。'
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {
          'mail':mail,
          'password':password
        }
        return render_template('login.html',error=error,data=input_data)
    
@app.route('/logout')
def logout():
  session.pop('user', None) # session の破棄
  session.pop('user_id', None) # session の破棄
  return render_template('index.html')
      
@app.route('/post')
def post():
  post_list = db.get_all_post()
  return render_template('post.html',post_list = post_list,name="/static/img/",user_id=session['user_id'])

@app.route('/register_post',methods=['POST'])
def register_post():
    if 'user' in session:
      post = request.form.get('post')
      cleaned_post = post.replace(" ", "")
      if cleaned_post == '':
        msg = '投稿内容が空白でした'
        post_list = db.get_all_post()
        return render_template('post.html',msg=msg,post_list = post_list,name="/static/img/")
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
        return redirect('/post')
      else:
        if(db.get_extension(file.filename)):
          file.save('static/img/'+file.filename)
          extension = db.get_extension(file.filename)
          db.user_post_img(user_id,post,prefecture_number,file.filename,extension)
          return redirect('/post')
        else:
          msg = '対応していない拡張子のファイルがふくまれています'
          post_list = db.get_all_post()
          return render_template('post.html',msg=msg,post_list = post_list,name="/static/img/")
    else :
      return redirect(url_for('login'))

@app.route('/mypage')
def mypage():
  if 'user' in session:
    user_id = session['user_id']
    id = user_id
    joy = advice_emotion_db.get_emotion1(user_id)
    anger = advice_emotion_db.get_emotion2(user_id)
    sadness = advice_emotion_db.get_emotion3(user_id)
    plesure = advice_emotion_db.get_emotion4(user_id)

    print(joy)
    
    if (joy[0] != 0 or anger[0] != 0 or sadness[0] != 0 or plesure[0] != 0):
      categories = ['喜', '怒', '哀', '楽']
      values = [joy[0],anger[0],sadness[0],plesure[0]]
      plt.bar(categories, values)
      id = str(id)
      graph_path = r'static/img/'+id+'.png'
      db.update_graph(graph_path,user_id)
      plt.savefig(graph_path)
      advice_emotion_db.register_coordinate(joy[0],anger[0],sadness[0],plesure[0],user_id)
      
      get_coordinate = advice_emotion_db.get_coordinate(user_id)
      get_advice = advice_emotion_db.view_advice(get_coordinate[0],get_coordinate[1])
      print(get_advice)
      post_list = db.get_my_post(user_id)
      graph = db.get_graph_path(user_id)
      return render_template('mypage.html',post_list = post_list,name="/static/img/",graph_name=graph[0],advice=get_advice)
    else:
      post_list = db.get_my_post(user_id)
      return render_template('mypage.html',post_list = post_list,name="/static/img/")
  else:
    return redirect(url_for('login'))

@app.route('/delete_post',methods=['POST'])
def delete_post():
   post_id = request.form.get('post_id')
   user_id = session['user_id']
   db.delete_post(post_id,user_id)
   id = user_id
   joy = advice_emotion_db.get_emotion1(user_id)
   anger = advice_emotion_db.get_emotion2(user_id)
   sadness = advice_emotion_db.get_emotion3(user_id)
   plesure = advice_emotion_db.get_emotion4(user_id)
   print(joy)
   if (joy[0] != 0 or anger[0] != 0 or sadness[0] != 0 or plesure[0] != 0):
    categories = ['喜', '怒', '哀', '楽']
    values = [joy[0],anger[0],sadness[0],plesure[0]]
    plt.bar(categories, values)
    id = str(id)
    graph_path = r'static/img/'+id+'.png'
    db.update_graph(graph_path,user_id)
    plt.savefig(graph_path)
    advice_emotion_db.register_coordinate(joy[0],anger[0],sadness[0],plesure[0],user_id)
      
    get_coordinate = advice_emotion_db.get_coordinate(user_id)
    get_advice = advice_emotion_db.view_advice(get_coordinate[0],get_coordinate[1])
    post_list = db.get_my_post(user_id)
    graph = db.get_graph_path(user_id)
    return render_template('mypage.html',post_list = post_list,name="/static/img/",graph_name=graph[0],advice=get_advice)
  #  post_list = db.get_my_post(user_id)
  #  return render_template('mypage.html',post_list = post_list,name="/static/img/")
  

# パスワード再設定画面の表示
@app.route('/mail')
def mail():
    return render_template('mail.html')

# 入力されたメールアドレスを確認してメールを送る
@app.route('/send_mail', methods=['POST'])
def send_mail():
    email = request.form.get('email')
    if db.check_email_exists(email):
        
        # メールアドレスをセッションに保存
        session['email'] = email
        session.permanent = True # session の有効期限を有効化
        app.permanent_session_lifetime = timedelta(minutes=30)# session の有効期限を5 分に設定
        return render_template('send_mail.html', email=email)
    else:
        return render_template('mail.html', message='メールアドレスが存在しません。')
      
#　セッションを確認する
@app.route('/password_change')
def password_change():
    if 'email' in session:
      return render_template('password_change.html')
    else:
      return redirect(url_for('login'))                        

# 入力された２つのパスワードを確認し、パスワードを変更
@app.route('/password_reset', methods=['POST'])
def password_reset():
    user_mail = session.get('email')
    password = request.form.get('password')
    password_check = request.form.get('password_check')

    # パスワードが一致しているか確認
    # 入力されていない場合
    if password == '' or password_check == '':
        return render_template('password_change.html', message='パスワードが入力されていません。')
    # 入力内容が一致していない場合
    elif password != password_check:
        return render_template('password_change.html', message='パスワードが一致しません。')
    # 入力内容が一致している場合
    elif password == password_check:
        # パスワードを変更
        session.pop('email', None) # session の破棄
        db.reset_password(password,user_mail)
        return render_template('password_reset.html',password=password)
    # それ以外の場合
    else:
        return render_template('password_change.html', message='パスワードが一致しません。')

#感情の追加
@app.route('/add_emotion',methods=['POST'])
def add_emotion():
  try:
    data = request.get_json()
    user_id = data.get('user_id')
    post_id = data.get('post_id')
    emotion = data.get('emotion')
    result = db.get_emotionos(user_id,post_id)
    print(user_id)
    print(post_id)
    print(emotion)
    # ユーザーが過去に押したボタンのリストを作成
    exist_emotions = set()
    if not result:
       print("実行2")
       db.add_emotions(user_id,post_id,emotion)
       return jsonify({'message':'Success'})   
    elif result:
      for db_exist in result:   
        print("存在する＝",db_exist)   
        exist_emotions.add(db_exist[3])
      print("exist=",exist_emotions)
      # ユーザーが押したタグがリストの中になければタグ付けする
      if int(emotion) not in exist_emotions:
        db.add_emotions(user_id,post_id,emotion)
        return jsonify({'message':'これまで押したことのないタグを登録するよ'})
      elif result[1] == user_id and result[2] == post_id and result[3] == emotion:
        # db.delete_emotion(user_id,post_id,emotion)
        return jsonify({'message':'タグ付けを解除する予定'})
  except Exception as e:
    print('実行3')
    return jsonify({'error':str(e)})
  return jsonify({'error':"未知のケースです"})


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
      user_list = admin_db.get_users()
      return render_template('account_management.html',user_list=user_list)
    else :
        error = 'ログインに失敗しました。'
        # dictで返すことでフォームの入力量が増えても可読性が下がらない。
        input_data = {
          'mail':mail,
          'password':password
        }
        return render_template('admin_login.html',error=error,data=input_data)

@app.route('/advice',methods=['GET'])
def advice():
  return render_template('register_advice.html')
  
@app.route('/register_advice',methods=['POST'])
def register_advice():
  advice = request.form.get('advice')
  emotional_x = request.form.get('x')
  emotional_y = request.form.get('y')
  count = admin_db.register_advice(advice,emotional_x,emotional_y)
  if count == 1:
    return render_template('register_advice.html')
  else:
    msg = '登録できませんでした。'
    return render_template('register_advice.html',msg=msg)
    
#ユーザー一覧
@app.route('/account_management',methods=['GET'])
def account_management():
  user_list = admin_db.get_users()
  return render_template('account_management.html',user_list=user_list)

# ユーザ削除
@app.route('/user_delete',methods=['POST'])
def user_delete():
    user_id = request.form.get('user_id')
    admin_db.user_delete(user_id)
    return redirect(url_for('account_management'))

if __name__ == '__main__':
  app.run(debug=True)
