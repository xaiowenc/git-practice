from flask import Flask, render_template
import re

app = Flask(__name__)

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
    else:
        return render_template("405.html")

@app.errorhandler(404)
def hello(error):
    return render_template("404.html")

if  __name__ == "__main__":
    app.debug = True
    app.run()
