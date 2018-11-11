#dbMgr.py
import pymysql

def getConnection():
    conn = pymysql.connect(host='192.168.34.121', port=3307, user='root', password ='1234', db='python_db', charset='utf8', autocommit=True,cursorclass=pymysql.cursors.DictCursor)
    # 딕셔너리 형태로 변경하여 가져온다
    return conn #연결 객체
#DB의 정보를 가져온다 / DB에 접속하는 정보

def board_write(data):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "INSERT INTO board(name,title,content,pwd) VALUES(%s,%s,%s,%s)"
    affected = cursor.execute(sql,data)
    cursor.close()
    conn.close()
    return affected

def sign_write(data):
    conn = getConnection()
    cursor = conn.cursor()
    sql = "INSERT INTO signin(name,age,pwd) VALUES(%s,%s,%s)"
    affected = cursor.execute(sql,data)
    cursor.close()
    conn.close()
    return affected

def board_list():
    rows = None
    try:
        conn =getConnection()
        cursor = conn.cursor()
        sql = "SELECT * FROM board ORDER BY num DESC"
        cursor.execute(sql)
        rows =cursor.fetchall()
        cursor.close()
    except Exception as e:
        print("err =================",e)
    finally:
        conn.close()     #연결을 얻었으면 반드시 close를 해줘야 한다
    return rows

    # 오류가 발생하지 않도록 try, excpet, finally 를 작성해 에러코드를 파악 할 수 있다.
    # 자원을 얻은 후 사용한 뒤 버리는 Proess
    # connection pool 을 이용해 자원을 버리지 않고 재사용 하는 Procss를 사용 (현장에서 connection pool방식을 이용한다.)

def board_read(num): #num을 받아온다
    row = None   #반환할 객체 (반환객체가 여러개일땐, rows)
    try:
        conn = getConnection()  # getConnection으로 연결객체를 얻는다.
        cursor = conn.cursor()  # 커서 객체를 가져온다
        sql = "SELECT * FROM board WHERE num=%s"  # 글번호 num을 불러온다
        cursor.execute(sql,(num))  # sql을 실행시킨다 /튜플로 넣어야 하므로 (num)을 사용
        row = cursor.fetchone()  #하나의 객체만 불러오는 경우

    except Exception as e:
        print("Read Error==========================================",e)
    finally:
        conn.close()
    return row

def board_hit_up(num):
    try:
        conn = getConnection()
        cursor =conn.cursor()
        sql = "UPDATE board set hit=hit+1 WHERE num=%s"
        data = (num)
        cursor.execute(sql, data)
        cursor.close()
    except Exception as e :
        print("'Hit up ============================================",e)
    finally:
        conn.close

def board_update(data):
    result = None
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = """
        update board
        set name = %s, title = %s ,content = %s, regdate =now()
        where num = %s and pwd = %s
        """
        result = cursor.execute(sql, data)
        cursor.close()
    except Exception as e:
        print('board_update err===================', e )
    finally:
        conn.close()
    return result

def board_delete(data):
    result = None
    try:
        conn =getConnection()
        cursor =conn.cursor()
        sql = "DELETE FROM board WHERE num =%s AND pwd=%s"
        result = cursor.execute(sql, data)
        cursor.close()
    except Exception as e:
        print('board_delete err=', e)
    finally:
        conn.close()
    return result


def comment_insert(data):
    result = None
    try :
        conn = getConnection()
        cursor = conn.cursor()
        sql = "INSERT INTO comments(c_name,c_content,num) VALUES(%s,%s,%s)"
        result = cursor.execute(sql,data)
        cursor.close()
    except Exception as e :
        print("comment_insert err==============================",e)
    finally:
        conn.close()
    return result

def comment_list(num):
    rows = None
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT * FROM comments WHERE num=%s ORDER BY c_no DESC"
        cursor.execute(sql, (num))
        rows = cursor.fetchall()
    except Exception as e :
        print('comment_list err==================',e)
    finally:
        conn.close()
    return rows

def board_count():
    result = None
    try :
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT count(*) cnt FROM board"
        cursor.execute(sql)
        result = cursor.fetchone()
    except Exception as e :
        print("board_count err ==================================",e)
    finally:
        conn.close()
    return result

def board_list_limit(data):
    rows = None
    try:
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT * FROM board ORDER BY num DESC LIMIT %s, %s"
        cursor.execute(sql, data)
        cursor.execute(sql, data)
        rows = cursor.fetchall()
    except Exception as e :
        print('board_list_limit err============================', e)
    finally:
        conn.close()
    return rows

if __name__ =='__main__':
    pass

'''
    data = ('12','12','23')
    res = board_list_limit(data)
    print(res)


    def test_guest():
        conn = getConnection()
        cursor = conn.cursor()
        sql = "SELECT * FROM guest"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        print(result)
'''
