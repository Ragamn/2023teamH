from dotenv import load_dotenv
import os,mysql.connector,string,random,hashlib
load_dotenv()
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASSE")
    }
#パスワードをハッシュする関数
def get_hash(password):
    hashed_password  = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

#ユーザを登録する関数
def register_user(user_name,user_mail,password):
    hashed_password = get_hash(password)
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO user(user_id,user_name,user_mail,user_pass,flag,graph_path,advice_kinds,emotional_x,emotional_y) VALUES(default,%s,%s,%s,default,/img/test1.png,default,0.5,0.5)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_name,user_mail,hashed_password))
        count = cursor.rowcount
        connection.commit

    except mysql.connector.Error:
        count = 0
    except Exception:
        count = 0
    finally:
        # カーソルを閉じる
        cursor.close()
        connection.close()

    return count

#ログイン関数
def user_login(user_mail,password):
    flg = False
    try:
        
        connection = mysql.connector.connect(**config)

        query = 'SELECT user_pass FROM user WHERE user_mail = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_mail,))
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
