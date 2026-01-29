from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Date, DateTime, ForeignKey, String, Text, Float, func
from datetime import date

class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)

class MoodRecord(Base):
    __tablename__ = 'mood_records'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    date: Mapped[str] = mapped_column(default=lambda: date.today().isoformat())
    mood: Mapped[str] = mapped_column()  
    emoji: Mapped[str] = mapped_column() 

class Homework(Base):
    __tablename__ = 'homeworks'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column()
    lesson: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    deadline: Mapped[date] = mapped_column(Date, nullable=True)
    is_expired: Mapped[bool] = mapped_column(default=False)

class HomeworkProgress(Base):
    __tablename__ = 'homework_progress'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column()
    completed_count: Mapped[int] = mapped_column(default=0)
    expired_count: Mapped[int] = mapped_column(default=0)