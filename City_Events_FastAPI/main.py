from datetime import datetime
import secrets
from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, EmailStr

# Подключаю стандартные инструменты SQLAlchemy для работы с базой данных
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship

# Инициализирую приложение
app = FastAPI()

# Заголовок для проверки авторизации пользователей по токену
API_KEY_NAME = "X-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# --- НАСТРОЙКА И ПОДКЛЮЧЕНИЕ БАЗЫ ДАННЫХ ---

# Указываю файл, где будут храниться все таблицы прямо на диске
DATABASE_URL = "sqlite:///./app_database.db"

# Создаю движок подключения и настраиваю фабрику сессий
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- ОПИСАНИЕ СТРУКТУРЫ ТАБЛИЦ (ОРМ МОДЕЛИ) ---

# Промежуточная таблица-связка для реализации логики "Многие-ко-многим" (Юзеры <-> События)
event_user_association = Table(
    "event_user",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True)
)


class UserDB(Base):
    """Таблица для хранения профилей пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Пароль пользователя
    token = Column(String, unique=True, nullable=True)  # Сюда пишется активный API-токен
    is_admin = Column(Boolean, default=False)  # Маркер администратора системы

    # Автоматическая связь: список событий, на которые записан этот человек
    events = relationship("EventDB", secondary=event_user_association, back_populates="users")


class EventDB(Base):
    """Таблица для хранения информации о событиях в городе"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    meeting_time = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)

    # Автоматическая связь: список людей, которые пойдут на этот ивент
    users = relationship("UserDB", secondary=event_user_association, back_populates="events")


# Команда автоматически проверяет структуру и создает файл app_database.db со всеми таблицами
Base.metadata.create_all(bind=engine)


# --- ВАЛИДАЦИЯ ДАННЫХ (Pydantic схемы для запросов и ответов) ---

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True  # Позволяет Pydantic читать данные напрямую из объектов SQLAlchemy


class EventResponse(BaseModel):
    id: int
    name: str
    meeting_time: datetime
    description: str
    users: List[UserResponse]  # Сюда автоматически подгрузится список участников

    class Config:
        from_attributes = True


# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ И ДЕПЕНДЕНСЫ ---

def get_db():
    """Открывает чистое соединение с базой на один запрос и закрывает его в конце"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(api_key_header), db: Session = Depends(get_db)) -> UserDB:
    """Проверяю токен из X-Token в базе данных. Возвращаю объект юзера"""
    if not token:
        raise HTTPException(status_code=401, detail="Передайте API токен в заголовке X-Token")

    user = db.query(UserDB).filter(UserDB.token == token).first()
    if not user:
        raise HTTPException(status_code=401, detail="Указан неверный или просроченный токен")
    return user


def get_current_admin(current_user: UserDB = Depends(get_current_user)) -> UserDB:
    """Проверка флага суперпользователя"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Действие доступно исключительно администраторам")
    return current_user


# --- РАБОЧИЕ МАРШРУТЫ API (ЭНДПОИНТЫ) ---

@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Регистрация нового профиля с автоматической выдачей токена"""
    if db.query(UserDB).filter(UserDB.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже зарегистрирован")
    if db.query(UserDB).filter(UserDB.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Этот email-адрес уже занят")

    generated_token = secrets.token_hex(16)

    new_user = UserDB(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password,
        token=generated_token,
        is_admin=False
    )

    db.add(new_user)
    db.commit()  # Сохраняем изменения в файл базы данных

    return {
        "message": "Вы успешно зарегистрировались",
        "username": new_user.username,
        "your_api_token": generated_token
    }


@app.get("/api/users", response_model=List[UserResponse])
def get_all_users(admin: UserDB = Depends(get_current_admin), db: Session = Depends(get_db)):
    """Выгрузка всех аккаунтов из базы (доступно только админу)"""
    return db.query(UserDB).all()


@app.get("/api/events", response_model=List[EventResponse])
def get_active_events(db: Session = Depends(get_db)):
    """Запрос списка предстоящих событий (фильтрация даты через SQL)"""
    now = datetime.now()
    # Запрос в БД эквивалентен команде: SELECT * FROM events WHERE meeting_time > текущее_время
    return db.query(EventDB).filter(EventDB.meeting_time > now).all()


@app.post("/api/event/{event_id}")
def subscribe_to_event(event_id: int, current_user: UserDB = Depends(get_current_user), db: Session = Depends(get_db)):
    """Запись текущего пользователя на выбранный ивент"""
    event = db.query(EventDB).filter(EventDB.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Запрашиваемое событие не найдено")

    if event.meeting_time <= datetime.now():
        raise HTTPException(status_code=400, detail="Событие уже завершено, запись закрыта")

    if current_user in event.users:
        return {"message": "Вы уже находитесь в списке участников"}

    # Добавляем связь между объектами, SQLAlchemy сам сделает запись в таблицу связей
    event.users.append(current_user)
    db.commit()
    return {"message": f"Вы успешно записались на событие '{event.name}'"}


@app.get("/api/events/my", response_model=List[EventResponse])
def get_my_events(current_user: UserDB = Depends(get_current_user)):
    """Просмотр списка всех моих подписок"""
    return current_user.events


# Автоматическое наполнение базы стартовыми данными при первом включении
@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    if db.query(EventDB).count() == 0:
        # Создаю дефолтного админа (логин: admin, пароль: adminpass, токен: admin-token)
        if not db.query(UserDB).filter(UserDB.username == "admin").first():
            admin = UserDB(
                username="admin", email="admin@local.ru",
                password="adminpass", token="admin-token", is_admin=True
            )
            db.add(admin)

        # Создаю два базовых события для теста
        db.add_all([
            EventDB(name="Танцы на набережной", meeting_time=datetime(2026, 9, 20, 18, 0), description="Уличные танцы"),
            EventDB(name="Сплав на каяках", meeting_time=datetime(2022, 5, 10, 10, 0), description="Прошлый тур")
        ])
        db.commit()
    db.close()
