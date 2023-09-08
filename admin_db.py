from dotenv import load_dotenv
import os,mysql.connector,string,random,hashlib
load_dotenv()
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE")
    }

#パスワードをハッシュ
def get_hash(password):
    hashed_password  = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

#管理者ログイン
def user_login(admin_mail,password):
    flg = False
    try:
        
        connection = mysql.connector.connect(**config)

        query = 'SELECT admin_pass FROM admin WHERE admin_mail = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(admin_mail,))
        get_pass = cursor.fetchone()
        hashed_password = get_hash(password)
        if hashed_password == get_pass[0]:
            flg = True
    except mysql.connector.Error:
        flg = False
    except Exception:
        flg = False
    finally:
        cursor.close()
        connection.close()

    return flg

# ユーザ一覧
def get_users():
    connection = mysql.connector.connect(**config)
    query = 'SELECT user_name FROM user where flag = 0'
    cursor = connection.cursor()
    cursor.execute(query,())
    cursor.close()
    connection.close()
    
# ユーザ削除
def user_delete(user_name):
    connection = mysql.connector.connect(**config)
    query = 'update user set flag = 1 where user_name = %s'
    cursor = connection.cursor()
    cursor.execute(query,(user_name,))
    cursor.close()
    connection.close()

#アドバイス登録
def register_advice(advice,emotional_x,emotional_y):
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO advice(id,advice,emotional_x,emotional_y) VALUES(default,%s,%s,%s)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(advice,emotional_x,emotional_y))
        count = cursor.rowcount
        connection.commit()

    except mysql.connector.Error:
        count = 0
    except Exception:
        count = 0
    finally:
        # カーソルを閉じる
        cursor.close()
        connection.close()

    return count