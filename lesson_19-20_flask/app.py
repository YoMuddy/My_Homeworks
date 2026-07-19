from flask import Flask, render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Создаем само веб-приложение
app = Flask(__name__)

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
        # If search is not empty, filter notes by title or content
        # ilike makes the search case-insensitive
        all_notes = Note.query.filter(
            (Note.title.ilike(f'%{search_query}%')) |
            (Note.content.ilike(f'%{search_query}%'))
        ).order_by(Note.date_created.desc()).all()  # Sort: newest first
    else:
        # If no search, just get all notes sorted from newest to oldest
        all_notes = Note.query.order_by(Note.date_created.desc()).all()

    # Pass the list of notes and the search query text to HTML
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


if __name__ == '__main__':
    # Просим Flask перед стартом проверить базу данных.
    # Если в нашей базе 'my_flask_db' еще нет таблицы 'note', она создастся автоматически по нашему чертежу
    with app.app_context():
        db.create_all()

    # Запускаем локальный веб-сервер в режиме разработчика (debug=True автоматически обновляет сайт при изменении кода)
    app.run(debug=True)
