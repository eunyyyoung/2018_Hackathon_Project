from flask import Flask , render_template, request, json,redirect, session
from models import dbMgr
from werkzeug import generate_password_hash
import pymysql
import math
#models 는 폴더명 , dbMgr 이라는 파이썬 파일이 정의되어 있다.
#__init__ : 객체를 만드는 생성자 이므로, 제작한 라이브러리 폴더에 꼭 존재해야 한다. (Python 관행)

def getConnection():
    conn = pymysql.connect(host='localhost', port=3307, user='root', password ='1234', db='python_db', charset='utf8', autocommit=True,cursorclass=pymysql.cursors.DictCursor)
    # 딕셔너리 형태로 변경하여 가져온다
    return conn #연결 객체
#DB의 정보를 가져온다 / DB에 접속하는 정보

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/writeform")
def writeform():
    return render_template('writeform.html')

@app.route("/write", methods=['POST'])
def write():
    print('넘어온 값들=======================',request.form)
    name = request.form['name']
    title = request.form['title']
    content = request.form['content']
    pwd = request.form['pwd']
    data = (name,title,content,pwd)
    dbMgr.board_write(data)
    return redirect('/list')

@app.route("/write2", methods=['POST'])
def write2():
	print('넘어온 값들====', request.form)
	name = request.form['name']
	age = request.form['age']
	pwd = request.form['pwd']
	data = (name,age,pwd)
	dbMgr.sign_write(data)
	return redirect('/')

@app.route("/list")
def list0():
    return redirect("/list/1")
    #글을 저장해 list.html에 뿌려준다
    #Model 에 역할을 나눠 코드가 간단해 졌다

# http://localhost:5000/list/17
@app.route("/list/<int:page>") # page를 숫자형으로 바꾼다 (정수형)
def list(page):
    size = 10  #10개식 페이지를 보여준다
    result = dbMgr.board_count()
    cnt = result['cnt']
    total_page = math.ceil(cnt/size) # ceil 올림하기 => 페이지 수에는 소수점이 없으므로
    begin = (page-1) * size #시작 글번호 선언
    data = (begin, size)
    rows = dbMgr.board_list_limit(data)
    link_size = 10                    # 링크를 10개씩 보여준다
    start_link = math.floor((page-1)/link_size) * link_size + 1
    end_link =start_link + (link_size - 1 )
    if end_link > total_page :
        end_link = total_page
    max = cnt - ((page-1)*link_size)
    print(type(rows))
    datas = {"rows":rows, "page":page, "total_page":total_page,"link_size":link_size,"start_link":start_link,"end_link":end_link,"max":max}

    return render_template('list.html' , datas=datas)

@app.route("/read/<num>/<page>")  #변수가 넘어올때 <>표시를 해준다. URL에 따라서 글이 온다
def read(num,page):
    dbMgr.board_hit_up(num)
    row = dbMgr.board_read(num)   # 따라온 글 번호를 넘긴다 , #dB에서 정의된 함수로  데이터를 불러온다.
    comments = dbMgr.comment_list(num)
    return render_template("read.html", row=row, comments=comments, page=page) #page라는 키에 넘어온 page값이 존재

@app.route("/updateform/<num>/<page>")
def updateform(num,page):
    row = dbMgr.board_read(num)
    return render_template('updateform.html', row=row,page=page)

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    return render_template('signUp.html')


@app.route("/update", methods=['POST'])
def update():
    print("T", request.form)
    num = request.form['num']
    name = request.form['name']
    title = request.form['title']
    content = request.form['content']
    pwd = request.form['pwd']
    page = request.form['page']
    data = ( name, title, content , num ,pwd )
    result = dbMgr.board_update(data)
    if result == 0 :
        return "<script>alert('비밀번호를 확인해 주세요 !');history.back();</script>"
    else :
        return redirect('/list/'+page)

@app.route("/deleteform/<num>/<page>")
def deleteform(num,page):
    return render_template('deleteform.html', num=num,page=page )

@app.route("/delete", methods=['POST'])
def delete():
    print('delete request.form ============',request.form)
    num = request.form['num']
    pwd = request.form['pwd']
    page = request.form['page']
    data = (num, pwd)
    result = dbMgr.board_delete(data)
    if result == 0 :
        return "<script>alert('비밀번호를 확인해 주세요 !');history.back();</script>"
    else :
        return redirect('/list/' + page)

@app.route("/commentform/<num>/<page>")
def commentform(num,page):
    return render_template('commentform.html', num=num,page=page)

@app.route("/comment",methods=['POST'])
def comment():
    print('comment request.form=========', request.form)
    num = request.form['num']
    name = request.form['name']
    content = request.form['content']
    page = request.form['page']
    data = (name, content, num)
    dbMgr.comment_insert(data)
    return redirect('/read/' + num+ '/'+ page)


@app.route("/showSignin")
def showSignin():
    return render_template('writeform2.html')

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['name']
        _password = request.form['password']

        conn= getConnection()
        cursor= conn.cursor()
        cursor.callproc('sp_validateLogin',(_username))
        data = cursor.fetchall()

        if len(data) > 0:
            if _password(str(data[0][3]),_password):
                session['name'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html',error = str(e))




if __name__ =='__main__':
    app.debug = True
    app.run()
