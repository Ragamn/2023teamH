from dotenv import load_dotenv
import os,mysql.connector,hashlib,requests
load_dotenv()
config = {
    "user": os.getenv("USER"),
    "password": os.getenv("PASS"),
    "host": os.getenv("HOST"),
    "database": os.getenv("DATABASE")
    }

# emotionsテーブルのuser_idからemotionの1(喜)取得
def get_emotion1(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT COUNT(emotion) FROM emotions WHERE user_id = %s AND emotion = 1'
        
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return 0
    except Exception as e:
        print(f"エラー: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()
        
# emotionsテーブルのuser_idからemotionの2(怒)を取得
def get_emotion2(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT COUNT(emotion) FROM emotions WHERE user_id = %s AND emotion = 2'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return 0
    except Exception as e:
        print(f"エラー: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()
        
# emotionsテーブルのuser_idからemotionの3(哀)を取得
def get_emotion3(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT COUNT(emotion) FROM emotions WHERE user_id = %s AND emotion = 3'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return 0
    except Exception as e:
        print(f"エラー: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()
        
# emotionsテーブルのuser_idからemotionの4(楽)を取得
def get_emotion4(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT COUNT(emotion) FROM emotions WHERE user_id = %s AND emotion = 4'

        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(user_id,))
        result = cursor.fetchone()

        return result
    except mysql.connector.Error as err:
        print(f"MySQLエラー: {err}")
        return 0
    except Exception as e:
        print(f"エラー: {e}")
        return 0
    finally:
        cursor.close()
        connection.close()

#ユーザー座標計算関数
def calculation(joy,anger,sadness,plesure):
    sum = anger+joy
    result_x = anger/sum
    sum = sadness+plesure
    result_y = plesure/sum
    return result_x,result_y


#ユーザー感情座標登録
def register_coordinate(joy,anger,sadness,plesure,user_id):
    try:
        result = calculation(joy,anger,sadness,plesure)
        connection = mysql.connector.connect(**config)
        query = "update user SET emotional_x = %s,emotional_y = %s WHERE user_id = %s"
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(result[0],result[1],user_id))
        print(result)
        print(result[0])
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

def get_coordinate(user_id):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT emotional_x,emotional_y FROM user WHERE user_id = %s'

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

def view_advice(x,y):
    try:
        connection = mysql.connector.connect(**config)
        query = 'SELECT advice FROM advice WHERE emotional_x BETWEEN %s AND %s AND emotional_y BETWEEN %s AND %s LIMIT 1'
        # クエリの実行
        cursor = connection.cursor()
        cursor.execute(query,(x-0.1,x+0.1,y-0.1,y+0.1))
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
    