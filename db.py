import os,mysql.connector,string,random,hashlib
config = {
    "user": "root",
    "password": "Trsm1107",
    "host": "localhost",
    "database": "anunaki"
    }
#パスワードをハッシュする関数
def get_hash(password):
    b_pw = bytes(password, 'utf-8')
    hashed_password  = hashlib.pbkdf2_hmac('sha256', b_pw,1000).hex()
    return hashed_password

#ユーザを登録する関数
def register_user(user_name,user_mail,password):
    hashed_password = get_hash(password)
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO user VALUES(default,%s,%s,%s,default,/img/test1.png,default,0.5,0.5)"

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