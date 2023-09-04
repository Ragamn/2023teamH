from flask import Flask, render_template,request,redirect,url_for,session
import db,string,random,os
from datetime import timedelta
from werkzeug.utils import secure_filename

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

if __name__ == '__main__':
    app.run(debug=True)