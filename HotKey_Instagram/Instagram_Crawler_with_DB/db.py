import pymysql
def access_db():
    # db 연결정보
    host = 'hotkey.czighwjgpkkz.ap-northeast-2.rds.amazonaws.com'
    user = 'admin'
    pw = 'hotkey123'
    port = 3306

    conn = pymysql.connect(host=host, user=user, password=pw, port=port, charset='utf8')  # db연결
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute('use hotkey;')
    return conn, cur

def close_db(conn):
    conn.commit()
    conn.close()