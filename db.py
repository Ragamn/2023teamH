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

        query = "INSERT INTO user(user_id,user_name,user_mail,user_pass,flag,graph_path,advice_kinds,emotional_x,emotional_y) VALUES(default,%s,%s,%s,default,'/img/test1.png',default,default,default)"

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

def get_flg(user_mail):
    flg = False
    try:
        
        connection = mysql.connector.connect(**config)

        query = 'SELECT flag FROM user WHERE user_mail = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_mail,))
        get_pass = cursor.fetchone()
        if 0 == get_pass[0]:
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
        query = 'SELECT post.post_id,user.user_name,post.post,post.good,post.prefecture_id,post.media_path,post.created_at,post.extension FROM post INNER JOIN user ON user.user_id = post.user_id WHERE post.flag = 0 ORDER BY post.post_id DESC'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query)
        result = []
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

            if file_extension in ['png','jpg','gif']:
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
        query = 'SELECT post.post_id,user.user_name,post.post,post.good,post.prefecture_id,post.media_path,post.created_at,post.extension FROM post INNER JOIN user ON user.user_id = post.user_id WHERE post.flag = 0 AND post.user_id = %s ORDER BY post.post_id DESC'

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

#感情重複しないための閲覧
def get_emotionos(user_id,post_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT id,user_id,post_id,emotion FROM emotions WHERE user_id = %s AND post_id = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post_id))
        result = cursor.fetchall()
        print("get_emoのresult=",result)
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

def delete_emotion(user_id,post_id,emotion):
    try:
        connection = mysql.connector.connect(**config)
        query = 'delete * FROM emotions WHERE user_id = %s AND post_id = %s AND emotion = %s'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,post_id,emotion))
        result = cursor.fetchall()
        print("del_emoのresult=",result)
        return None
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# 登録してあるメールアドレスの検索
def check_email_exists(email):
    try:
        # データベースに接続
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # メールアドレスを検索
        cursor.execute("SELECT * FROM user WHERE user_mail = %s", (email,))
        user = cursor.fetchone()

        if user is None:
            return False
        else:
            return True

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        # 接続をクローズ
        if connection.is_connected():
            cursor.close()
            connection.close()

def reset_password(password,user_mail):
    hashed_password = get_hash(password)
    try:
        # データベースに接続
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # パスワードを更新
        query = "UPDATE user SET user_pass = %s WHERE user_mail = %s"
        cursor.execute(query,(hashed_password,user_mail,))
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error: {error}")
    finally:
        # 接続をクローズ
        if connection.is_connected():
            cursor.close()
            connection.close()

#投稿削除機能
def delete_post(post_id,user_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        delete_query = "UPDATE post SET flag = 1 WHERE post_id = %s AND user_id = %s"
        cursor.execute(delete_query, (post_id,user_id))

        connection.commit()
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

#グラフ登録
def update_graph(graph_path,user_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        query = "UPDATE user SET graph_path = %s WHERE user_id = %s"
        cursor.execute(query, (graph_path,user_id))

        connection.commit()
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        cursor.close()
        connection.close()

#グラフパス取得
def get_graph_path(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT graph_path FROM user WHERE user_id = %s'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
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

#感情リアクションの値取り出し
def joy_count(post_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT count(*) FROM emotions WHERE post_id = %s AND emotion = 1'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(post_id,))
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

def anger_count(post_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT count(*) FROM emotions WHERE post_id = %s AND emotion = 2'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(post_id,))
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

def sadness_count(post_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT count(*) FROM emotions WHERE post_id = %s AND emotion = 3'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(post_id,))
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

def plesure_count(post_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT count(*) FROM emotions WHERE post_id = %s AND emotion = 4'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(post_id,))
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

#投稿のid取得関数
def get_post_id():
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT post_id FROM emotions WHERE flag = 0'
        
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

def get_many_emotion():
    try:
        connection = mysql.connector.connect(**config)
        query1 = 'SELECT emotion, count(*) as count from emotions GROUP BY emotion order by count desc limit 1'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query1)
        result1 = cursor.fetchone()

        query2= 'SELECT prefecture, emotion, COUNT(*) AS count FROM post as p INNER JOIN emotions AS e on p.post_id = e.post_id INNER JOIN prefecture AS pr on p.prefecture_id = pr.id WHERE emotion = %s GROUP BY prefecture_id, emotion ORDER BY COUNT DESC LIMIT 1'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query2,(result1[0],))
        result2 = cursor.fetchone()

        return result2
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
    finally:
        cursor.close()
        connection.close()