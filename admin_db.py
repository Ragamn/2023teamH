from dotenv import load_dotenv
import os,mysql.connector,string,random,hashlib
load_dotenv()
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASSE")
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

        query = 'SELECT admin_pass FROM user WHERE admin_mail = %s'

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