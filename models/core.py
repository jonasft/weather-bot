import os
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import datetime

Base = declarative_base()


class Execution(Base):
    __tablename__ = "execution"
    id = Column(Integer, primary_key=True)
    date_executed = Column(Date, default=datetime.date.today)
    forecasts = relationship("Forecast", back_populates="execution")


class Forecast(Base):
    __tablename__ = "forecast"
    id = Column(Integer, primary_key=True)
    execution_id = Column(Integer, ForeignKey("execution.id"))
    created = Column(DateTime, default=datetime.datetime.utcnow)
    timestamp = Column(DateTime)
    wind_speed = Column(Float)
    wind_from_direction = Column(Float)
    direction = Column(String)
    is_above_threshold = Column(Boolean)
    execution = relationship("Execution", back_populates="forecasts")


# Setup the database connection
database_url = os.getenv("DATABASE_URL", "sqlite:///./data.db")
engine = create_engine(database_url)
Base.metadata.create_all(engine)


# Create a session
Session = sessionmaker(bind=engine)


import datetime
from sqlalchemy.orm.exc import NoResultFound


def add_forecast_data(wind_data):
    session = Session()
    try:
        # Check if an execution for today already exists
        today = datetime.date.today()
        try:
            execution = session.query(Execution).filter_by(date_executed=today).one()
        except NoResultFound:
            # If not, create a new execution
            execution = Execution()
            session.add(execution)
            session.commit()

        for data_point in wind_data:
            timestamp, wind_speed, wind_from_direction = data_point
            forecast = Forecast(
                execution_id=execution.id,
                timestamp=datetime.datetime.fromisoformat(timestamp),
                wind_speed=wind_speed,
                wind_from_direction=wind_from_direction,
            )
            session.add(forecast)
        session.commit()
    except Exception as e:
        print("An error occurred:", e)
        session.rollback()
    finally:
        session.close()
