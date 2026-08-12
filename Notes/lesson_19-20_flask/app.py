from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta


# Создаем само веб-приложение
app = Flask(__name__)

# Конфигурация для работы сессий и JWT
app.config['SECRET_KEY'] = 'secret-session-key-123'
app.config["JWT_SECRET_KEY"] = "secret-jwt-key-456"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# Инициализация JWT
jwt = JWTManager(app)


# Middleware для автоматического логирования активности пользователей
@app.before_request
def log_user_activity():
    # Получаем имя пользователя из сессии (или AnonymousUser, если не вошел)
    username = session.get('username', 'AnonymousUser')

    # Получаем текущее время в формате MM.DD.YYYY HH:MM
    now_str = datetime.now().strftime('%m.%d.%Y %H:%M')

    # Получаем полный URL запроса
    url_path = request.full_path

    # Формируем строку для лога
    log_entry = f"{now_str} | {username} | URL={url_path}\n"

    # Записываем строку в файл логов
    with open('usersActivity.log', 'a', encoding='utf-8') as f:
        f.write(log_entry)


# Прописываем секретный адрес для подключения к нашей базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/my_flask_db'

# Отключаем ненужное слежение за изменениями, чтобы компьютер не тормозил
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Объединяем Flask и базу данных в один рабочий инструмент 'db'
db = SQLAlchemy(app)


# ОБНОВЛЕННЫЙ ЧЕРТЕЖ ЗАМЕТКИ С КОЛОНКОЙ ДЛЯ ДАТЫ
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # default=datetime.now автоматически ставит текущее время компьютера при создании заметки
    date_created = db.Column(db.DateTime, default=datetime.now)


# ОБНОВЛЕННАЯ ГЛАВНАЯ СТРАНИЦА С ПОИСКОМ И СОРТИРОВКОЙ
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        title_from_form = request.form.get('title')
        content_from_form = request.form.get('content')

        new_note = Note(title=title_from_form, content=content_from_form)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('index'))

    # ПОИСК: ловим то, что пользователь ввёл в поисковую строку (по умолчанию строка пустая)
    search_query = request.args.get('search', '')

    if search_query:
        all_notes = Note.query.filter(
            (Note.title.ilike(f'%{search_query}%')) |
            (Note.content.ilike(f'%{search_query}%'))
        ).order_by(Note.date_created.desc()).all()
    else:
        all_notes = Note.query.order_by(Note.date_created.desc()).all()


    # ... ваш существующий код получения списка заметок (например, notes = Note.query.all()) ...

    # Получаем список ID просмотренных заметок из сессии
    viewed_ids = session.get('viewed_notes', [])

    # Достаем из базы данных только те заметки, которые есть в истории просмотров
    # Чтобы сохранить правильный порядок (от свежих к старым), сортируем их в Python
    if viewed_ids:
        # Получаем объекты заметок из базы данных
        history_notes_raw = Note.query.filter(Note.id.in_(viewed_ids)).all()
        # Выстраиваем их строго в том порядке, в каком ID лежат в сессии
        history_notes = sorted(history_notes_raw, key=lambda x: viewed_ids.index(x.id))
    else:
        history_notes = []

    # Передаем history_notes в ваш render_template главной страницы
    # Допишите , history_notes=history_notes внутрь вашей существующей строки возврата:
    return render_template('index.html', notes=all_notes, search_query=search_query)


# Маршрут для удаления заметки. В адресе <int:note_id> — это ID конкретной заметки
@app.route('/note/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    # Ищем заметку в базе по её ID. Если её нет — Flask выдаст ошибку 404
    note_to_delete = Note.query.get_or_404(note_id)

    # Даем команду базе данных удалить эту запись
    db.session.delete(note_to_delete)
    # Подтверждаем удаление (сохраняем изменения в PostgreSQL)
    db.session.commit()

    # Возвращаем пользователя на главную страницу
    return redirect(url_for('index'))


# Маршрут для редактирования. Работает и на показ формы (GET), и на сохранение изменений (POST)
@app.route('/note/<int:note_id>/edit', methods=['GET', 'POST'])
def edit_note(note_id):
    # Ищем нужную заметку в базе данных по её уникальному ID
    note_to_edit = Note.query.get_or_404(note_id)

    # Если пользователь заполнил форму новыми данными и нажал кнопку "Сохранить"
    if request.method == 'POST':
        # Перезаписываем старый заголовок и старый текст новыми значениями из полей формы
        note_to_edit.title = request.form.get('title')
        note_to_edit.content = request.form.get('content')

        # Сохраняем (коммитим) измененные данные обратно в PostgreSQL
        db.session.commit()

        # После успешного сохранения возвращаем пользователя на главную страницу
        return redirect(url_for('index'))

    # Если это обычный переход по ссылке (GET), показываем файл edit_note.html
    # и передаем туда нашу заметку, чтобы заполнить поля её текущим текстом
    return render_template('edit_note.html', note=note_to_edit)


# Маршрут для детального просмотра заметки и истории в сессиях
@app.route('/note/<int:note_id>')
def view_note(note_id):
    # Находим заметку в базе данных PostgreSQL по ID
    note = Note.query.get_or_404(note_id)

    # 1. Достаем текущий список просмотров из сессии
    history = session.get('viewed_notes', [])

    # 2. Если заметка уже есть в списке, убираем её оттуда
    if note_id in history:
        history.remove(note_id)

    # 3. Добавляем ID текущей заметки в самое начало (индекс 0)
    history.insert(0, note_id)

    # 4. Обрезаем список, если в нем накопилось больше 20 элементов
    if len(history) > 20:
        history.pop()

    # 5. Сохраняем обновленный список обратно в сессию
    session['viewed_notes'] = history
    session.modified = True

    return render_template('view_note.html', note=note)


# Эндпоинт для JWT-аутентификации (выдача токена доступа)
@app.route('/api/login', methods=['POST'])
def login_api():
    # Проверяем, что клиент прислал данные в формате JSON
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # Простая проверка данных пользователя (заглушка для лабораторной).
    # Если у вас в базе есть модель User, здесь можно сделать проверку по базе.
    if username != "admin" or password != "password":
        return jsonify({"msg": "Неверный логин или пароль"}), 401

    # Если всё верно, генерируем JWT-токен доступа
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

if __name__ == '__main__':
    # Просим Flask перед стартом проверить базу данных.
    # Если в нашей базе 'my_flask_db' еще нет таблицы 'note', она создастся автоматически по нашему чертежу
    with app.app_context():
        db.create_all()

    # Запускаем локальный веб-сервер в режиме разработчика (debug=True автоматически обновляет сайт при изменении кода)
    app.run(debug=True)
