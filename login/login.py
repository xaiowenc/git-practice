from flask import Flask, render_template, request, make_response
from redis import StrictRedis, ConnectionPool
import psycopg2, hashlib, time,re

app = Flask(__name__)


dicts = {}

@app.route('/save', methods=['GET', 'POST'])
def put_number():
    if request.method == 'POST' and func_user_validity():
        req_data = request.get_json(force=True)
        keys = req_data['key']
        values = req_data['value']
        if values.isdigit() and (not keys.isdigit()):
            dicts[keys] = values
            for key2, name2 in dicts.items():
                print(key2 + " " + name2 + " ")
            return "save OK"
        else:
            return "save fail"
    else:
        return "get...或使用者不存在"

@app.route('/load', methods=['GET'])
def load_number():
    keys = request.args.get('key')
    if keys in dicts and func_user_validity():
        return dicts[keys]
    else:
        return keys + " not found"

@app.route('/plus/<num1>/<num2>')
def show_plus(num1, num2):
    if func_user_validity():
        return method(num1, num2, '+')
    else:
        return "testing for func_user_validity()...使用者不存在"

@app.route('/sub/<num1>/<num2>')
def show_sub(num1, num2):
    return method(num1, num2, '-')

@app.route('/mul/<num1>/<num2>')
def show_mul(num1, num2):
    return method(num1, num2, '*')

@app.route('/div/<num1>/<num2>')
def show_div(num1, num2):
    return method(num1, num2, '/')

def method(num1, num2, op):
    value = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
    num1_f = value.match(num1)
    num2_f = value.match(num2)
    if (num1.isdigit() or num1_f) and (num2.isdigit() or num2_f):
        if op == '+':
            return 'num1 %s num2= %.2f' % (op, (float(num1) + float(num2)))
        if op == '-':
            return 'num1 %s num2= %.2f' % (op, (float(num1) - float(num2)))
        if op == '*':
            return 'num1 %s num2= %.2f' % (op, (float(num1) * float(num2)))
        if op == '/':
            return 'num1 %s num2= %.2f' % (op, (float(num1) / float(num2)))
    elif num1 in dicts and num2 in dicts:
        if op == '+':
            return 'num1 %s num2= %.2f' % (op, (float(dicts[num1]) + float(dicts[num2])))
        if op == '-':
            return 'num1 %s num2= %.2f' % (op, (float(dicts[num1]) - float(dicts[num2])))
        if op == '*':
            return 'num1 %s num2= %.2f' % (op, (float(dicts[num1]) * float(dicts[num2])))
        if op == '/':
            return 'num1 %s num2= %.2f' % (op, (float(dicts[num1]) / float(dicts[num2])))
    else:
        return render_template("405.html")


#驗證有該用戶
def func_checkACC(ac, pwd):
    conn = psycopg2.connect(database="test_db", user="postgres", password="123456", host="127.0.0.1", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT account, id, password FROM registration where account='{0}' and password='{1}'".format(ac, pwd)) #傳入多個參數
    rowlist = list(cur.fetchall())
    print("rowlist:", end = ' ')
    print(rowlist)
    
    if rowlist:
       print("login OK...")
       cur.close()
       conn.close()
       return 1
    else:
        print("login Fail...")
        cur.close()
        conn.close()
        return 0

#gen MD5(帳戶+當下日期時間)
def func_genHash(ac):
    localtime = time.asctime(time.localtime(time.time()))
    data = ac + localtime
    hash_data = hashlib.md5(data.encode("utf-8"))
    print(hash_data.hexdigest())
    return hash_data.hexdigest()

#儲存資料到redis 於redis保存十分鐘
#並且使用flask存於cookie中 瀏覽器關閉才結束cookie
def func_store_info(hashkey, user):
    r = StrictRedis(host='127.0.0.1', port=6379)
    r.set(hashkey, user, px=600000)

    #set cookie in Flask
    #一般是用這種方式嗎? Set-Cookie: https://developer.mozilla.org/zh-TW/docs/Web/HTTP/Cookies
    response = make_response("login OK...try another url") #make_response(render_template("register.html"))
    response.set_cookie("user", hashkey) #(hashkey, user)
    return response

#檢核cookie中的用戶是否存在redis中
def func_user_validity():
    r2 = StrictRedis(host='127.0.0.1', port=6379)
    if r2.get(request.cookies.get('user')):
        return 1
    else:
        print('no exit')
        return 0

#登入畫面
@app.route('/', methods=['GET','POST'])
def func_index():
    if request.method == 'POST':
        account_ = request.form.get('account')
        password_ = request.form.get('password')
        isOK = func_checkACC(account_, password_)
        if isOK:
            return func_store_info(func_genHash(account_), account_)
        else:
            return "login Fail..."
    else:
        return render_template("index.html")



#若key值無重複則塞資料
#for register
def func_insert(ac, id_, pwd):
    conn = psycopg2.connect(database="test_db", user="postgres", password="123456", host="127.0.0.1", port="5432")

    print(ac)
    print(type(ac))
    cur = conn.cursor()
    cur.execute("SELECT account, id, password FROM registration where account='{0}' or id='{1}'".format(ac, id_))
    rowlist = list(cur.fetchall())
    
    if rowlist:
        cur.close()
        conn.close()
        return 0
    else:
        cur.execute("insert into registration (account, id, password) values ('{0}', '{1}', '{2}')".format(ac, id_, pwd))
        conn.commit()
        cur.close()
        conn.close()
        return 1

#註冊畫面
@app.route('/register', methods=['GET','POST'])
def func_register():
    if request.method == 'POST':
        account_ = request.form.get('account')
        id_ = request.form.get('id')
        password_ = request.form.get('password')
        isOK = func_insert(account_, id_, password_)
        if isOK:
            return "register OK"
        else:
            return "account or id repeat..."
    else:
        return render_template("register.html")

@app.errorhandler(404)
def hello(error):
    return render_template("404.html")

if  __name__ == "__main__":
    app.debug = True
    app.run()
