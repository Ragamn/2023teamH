from dotenv import load_dotenv
import os,mysql.connector,hashlib,requests
load_dotenv()
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE")
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

        query = "INSERT INTO user(user_id,user_name,user_mail,user_pass,flag,graph_path,advice_kinds,emotional_x,emotional_y) VALUES(default,%s,%s,%s,default,'/img/test1.png',default,0.5,0.5)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_name,user_mail,hashed_password))
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

#利用者投稿関数(画像,動画がない場合)
def user_post(user_id,post,prefecture_id):
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO post(post_id,user_id,post,good,prefecture_id,media_path,flag) VALUES(default,%s,%s,default,%s,default,default)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post,prefecture_id))
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

#利用者投稿関数(画像,動画がある場合)
def user_post_img(user_id,post,prefecture_id,media_path):
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO post(post_id,user_id,post,good,prefecture_id,media_path,flag) VALUES(default,%s,%s,default,%s,%s,default)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post,prefecture_id,media_path))
        count = cursor.rowcount
        connection.commit()

    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        count = 0
    except Exception as e:
        print(f"エラー: {e}")
        count = 0
    finally:
        # カーソルを閉じる
        cursor.close()
        connection.close()

    return count

#ユーザID取得関数
def get_user_id(user_mail):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT user_id FROM user WHERE user_mail = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query, (user_mail,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

def get_location_from_latlng(latitude, longitude):
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        "format": "json",
        "lat": latitude,
        "lon": longitude,
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # HTTPエラーレスポンスがあれば例外を発生させます。
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        return f"エラーが発生しました: {str(e)}"
    
    
#投稿削除機能
def delete_user_posts(user_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # ログインしているユーザーに関連する投稿の論理削除フラグを設定
        delete_query = "UPDATE post SET flag = 1 WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        connection.commit()
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

    finally:
        cursor.close()
        connection.close()

