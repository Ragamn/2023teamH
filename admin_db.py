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
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT user_id,user_name FROM user where flag = 0'
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()  # クエリの結果を取得する

        return result
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"エラーが発生しました: {err}")

    finally:
        # 必ず接続をクローズする
            cursor.close()
            connection.close()
    
# ユーザ削除
def user_delete(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'UPDATE user SET flag = 1 WHERE user_id = %s'
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()  # 変更をコミット
        return True
    
    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"エラーが発生しました: {err}")
        return False

    finally:
        # 必ず接続をクローズする
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