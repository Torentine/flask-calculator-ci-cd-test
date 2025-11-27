from flask import Flask, request, render_template
import os

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/user/<username>')
def show_user(username):
    return f"Hello, {username}"

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f"Это пост под номером: {post_id}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        return f'Попытка входа: {username}'
    else:
        return '''
            <form method="post">
                Логин: <input name="username"><br>
                Пароль: <input name="password" type="password"><br>
                <button type="submit">Войти</button>
            </form>
        '''

@app.route('/calc', methods=['GET'])
def calculator():
    try:
        a_str = request.args.get('a', '0')
        b_str = request.args.get('b', '0')
        operation = request.args.get('operation', '+')
        
        # Исправляем проблему с пробелом вместо +
        if operation == ' ':
            operation = '+'
        
        # Обработка пустых строк
        a = float(a_str) if a_str != '' else 0
        b = float(b_str) if b_str != '' else 0
        
        if operation == '+':
            result = a + b
        elif operation == '-':
            result = a - b
        elif operation == '*':
            result = a * b
        elif operation == '/':
            if b == 0:
                return "Ошибка: деление на ноль"
            result = a / b
        else:
            return "Неверная операция"
        
        # Форматируем результат: убираем .0 для целых чисел
        if result.is_integer():
            return f"Результат: {int(result)}"
        else:
            return f"Результат: {result}"
    except ValueError:
        return "Ошибка: неверный формат числа"

if __name__ == '__main__':
    app.run(debug=True)