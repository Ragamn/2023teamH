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
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
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
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
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
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
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
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None
    finally:
        cursor.close()
        connection.close()