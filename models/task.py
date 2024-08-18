from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, timezone

DATABASE_URL = "postgresql://user:password@db/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hours = Column(Integer, nullable=False)
    minutes = Column(Integer, nullable=False)
    seconds = Column(Integer, nullable=False)
    url = Column(String, nullable=True)
    timer_triggered = Column(Boolean, default=False)
    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def get_expiration_time(self) -> datetime:
        expiration_delta = timedelta(
            hours=self.hours, minutes=self.minutes, seconds=self.seconds
        )
        if self.created_at.tzinfo is None:
            self.created_at = self.created_at.replace(tzinfo=timezone.utc)

        expiration_time = self.created_at + expiration_delta
        print(
            f"Created At: {self.created_at}, Expiration Delta: {expiration_delta}, Expiration Time: {expiration_time}"
        )

        return expiration_time

    def time_left(self) -> int:
        expiration_time = self.get_expiration_time()
        now = datetime.now(timezone.utc)
        print(f"Now: {now}, Expiration Time: {expiration_time}")
        remaining_time = expiration_time - now
        return max(0, int(remaining_time.total_seconds()))


def create_task(db, hours: int, minutes: int, seconds: int, url: str):
    new_task = Task(hours=hours, minutes=minutes, seconds=seconds, url=url)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def get_task(db, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()
