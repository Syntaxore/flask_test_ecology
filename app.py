from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_results.db'
db = SQLAlchemy(app)


# Модель для хранения результатов теста
class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, nullable=False)


# Список вопросов и вариантов ответов
questions = [
    {"question": "Как часто вы выключаете свет, когда уходите из комнаты?", "name": "q1",
     "options": ["Всегда", "Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Как часто вы используете общественный транспорт или велосипед?", "name": "q2",
     "options": ["Ежедневно", "Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Сортируете ли вы мусор?", "name": "q3", "options": ["Да", "Нет"]},
    {"question": "Потребляете ли вы меньше одноразового пластика?", "name": "q4", "options": ["Да", "Нет"]},
    {"question": "Поддерживаете ли вы экологические инициативы и программы?", "name": "q5", "options": ["Да", "Нет"]},
    {"question": "Как часто вы покупаете продукты с минимальной упаковкой?", "name": "q6",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Используете ли вы экологически чистые чистящие средства?", "name": "q7", "options": ["Да", "Нет"]},
    {"question": "Сколько раз в месяц вы проводите уборку для сбора мусора в общественных местах?", "name": "q8",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Как часто вы выбираете товары, произведенные местными производителями?", "name": "q9",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Как часто вы следите за экономией воды в доме?", "name": "q10",
     "options": ["Всегда", "Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Используете ли вы многоразовые сумки для покупок?", "name": "q11", "options": ["Да", "Нет"]},
    {"question": "Как часто вы утилизируете батарейки и электронные устройства?", "name": "q12",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Участвуете ли вы в программах по восстановлению зелёных насаждений?", "name": "q13",
     "options": ["Да", "Нет"]},
    {"question": "Как часто вы проверяете, не утечет ли вода из крана или трубы?", "name": "q14",
     "options": ["Всегда", "Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Соблюдаете ли вы правила по утилизации опасных отходов?", "name": "q15", "options": ["Да", "Нет"]},
    {"question": "Как часто вы готовите еду в большом количестве, чтобы сократить количество выбрасываемого пищи?",
     "name": "q16", "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Сколько раз в неделю вы покупаете продукты на оптовых рынках?", "name": "q17",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Как часто вы делаете выбор в пользу энергоэффективных устройств?", "name": "q18",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]},
    {"question": "Поддерживаете ли вы движение за защиту дикой природы?", "name": "q19", "options": ["Да", "Нет"]},
    {"question": "Как часто вы убираете мусор в своем районе?", "name": "q20",
     "options": ["Часто", "Иногда", "Редко", "Никогда"]}
]


# Оценки за каждый ответ
def get_score(answer):
    scores = {
        "Всегда": 5,
        "Часто": 4,
        "Иногда": 3,
        "Редко": 2,
        "Никогда": 1,
        "Да": 5,
        "Нет": 1
    }
    return scores.get(answer, 0)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enter_name', methods=['GET', 'POST'])
def enter_name():
    if request.method == 'POST':
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        return redirect(url_for('index'))
    return render_template('enter_name.html')


@app.route('/test', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        total_score = 0
        for i in range(1, 21):
            answer = request.form.get(f'q{i}', '')
            total_score += get_score(answer)

        new_result = TestResult(
            first_name=session.get('first_name', 'Anonymous'),
            last_name=session.get('last_name', 'Anonymous'),
            score=total_score
        )
        db.session.add(new_result)
        db.session.commit()

        return redirect(url_for('result'))

    if 'first_name' not in session or 'last_name' not in session:
        return redirect(url_for('enter_name'))

    return render_template('index.html', questions=questions)


@app.route('/result')
def result():
    if 'first_name' not in session or 'last_name' not in session:
        return redirect(url_for('enter_name'))

    # Поскольку данные уже сохранены в базе данных в маршруте /test, здесь просто показываем результат
    total_score = TestResult.query.order_by(TestResult.id.desc()).first().score

    # Определение сообщения
    if total_score > 55:
        message = "Отлично! Вы хорошо заботитесь о природе."
    elif total_score > 35:
        message = "Хорошо! Вы делаете много для охраны окружающей среды, но есть еще возможности для улучшения."
    elif total_score > 20:
        message = "Есть над чем поработать. Старайтесь больше заботиться о природе!"
    else:
        message = "Необходимо значительное улучшение. Применяйте больше усилий для защиты окружающей среды!"

    return render_template('result.html', score=total_score, message=message)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Проверка логина и пароля
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            return "Неверное имя пользователя или пароль"
    return render_template('admin_login.html')


@app.route('/admin/panel', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    if request.method == 'POST' and 'clear_logs' in request.form:
        TestResult.query.delete()
        db.session.commit()
        return redirect(url_for('admin_panel'))

    # Получение всех результатов тестов
    results = TestResult.query.all()
    return render_template('admin_panel.html', results=results)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
