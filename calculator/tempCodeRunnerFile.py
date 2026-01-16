from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    operation = request.form['operation']
    num1 = float(request.form['num1'])
    num2 = float(request.form['num2'])

    if operation == 'add':
        result = num1 + num2
    elif operation == 'subtract':
        result = num1 - num2
    elif operation == 'multiply':
        result = num1 * num2
    elif operation == 'divide':
        if num2 == 0:
            result = "Cannot divide by zero!"
        else:
            result = num1 / num2
    else:
        result = "Invalid operation"

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
