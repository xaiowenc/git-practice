from flask import Flask, render_template, request
import logging, re

app = Flask(__name__)

#handler = logging.FileHandler('app.log', encoding='UTF-8')
#app.logger.addHandler(handler)

dicts = {}

@app.route('/save', methods=['GET', 'POST'])
def put_number():
    if request.method == 'POST':
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
        return "get..."

@app.route('/load', methods=['GET'])
def load_number():
    keys = request.args.get('key')
    if keys in dicts:
        return dicts[keys]
    else:
        return keys + " not found"

@app.route('/plus/<num1>/<num2>')
def show_plus(num1, num2):
    return method(num1, num2, '+')

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

@app.errorhandler(404)
def hello(error):
    return render_template("404.html")

if  __name__ == "__main__":
    app.debug = True
    app.run()
