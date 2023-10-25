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
engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)
