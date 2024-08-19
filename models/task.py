from datetime import datetime, timedelta, timezone

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@db/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    expiration_time = Column(DateTime(timezone=True), nullable=False)
    task_triggered = Column(Boolean, default=False)

    def time_left(self) -> int:
        now = datetime.now(timezone.utc)
        remaining_time = self.expiration_time - now
        return max(0, int(remaining_time.total_seconds()))


def create_task(db, hours: int, minutes: int, seconds: int, url: str):
    created_at = datetime.now(timezone.utc)
    expiration_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    expiration_time = created_at + expiration_delta

    new_task = Task(url=url, created_at=created_at, expiration_time=expiration_time)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task(db, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()
