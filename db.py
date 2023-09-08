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

        query = "INSERT INTO post(post_id,user_id,post,good,prefecture_id,media_path,flag,extension) VALUES(default,%s,%s,default,%s,default,default,default)"

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
def user_post_img(user_id,post,prefecture_id,media_path,extension):
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO post(post_id,user_id,post,good,prefecture_id,media_path,flag,extension) VALUES(default,%s,%s,default,%s,%s,default,%s)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post,prefecture_id,media_path,extension))
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
    
#投稿一覧関数
def get_all_post():
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT post.post_id,user.user_name,post.post,post.good,post.prefecture_id,post.media_path,post.created_at,post.extension FROM post INNER JOIN user ON user.user_id = post.user_id WHERE post.flag = 0'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

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

#ファイル判断関数
def get_extension(filename):
    try:
        if isinstance(filename,str):
            # ファイル名を小文字に変換して、拡張子を取得します
            file_extension = filename.lower().split('.')[-1]

            if file_extension in ['png','jpg']:
                return 1
            elif file_extension == 'mp4':
                return 2
            elif file_extension in ['wav','mp3']:
                return 3
            else:
                return False
    except IndexError:
        # '.'がファイル名に含まれていない場合など、IndexErrorが発生する可能性があります
        return False
    
#自分の投稿閲覧関数
def get_my_post(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT post.post_id,user.user_name,post.post,post.good,post.prefecture_id,post.media_path,post.created_at,post.extension FROM post INNER JOIN user ON user.user_id = post.user_id WHERE post.flag = 0 AND post.user_id = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
        result = cursor.fetchall()

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

#感情追加
def add_emotions(user_id,post_id,emotion):
    try:
        
        connection = mysql.connector.connect(**config)

        query = "INSERT INTO emotions(id,user_id,post_id,emotion) VALUES(default,%s,%s,%s)"

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post_id,emotion))
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