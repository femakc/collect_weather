from sqlalchemy import (ForeignKey, Integer, String,
                        DateTime, Boolean, Column, Float)
from sqlalchemy.orm import declarative_base, relationship, Mapped

Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    temp = Column(Integer)
    timestamp = Column(Integer)
    # city = relationship("City", uselist=False, back_populates="city")


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    country = Column(String)
    population = Column(Integer)
    is_capital = Column(Boolean)
    weather_id = Column(Integer, ForeignKey("weather.id"))
    weather = relationship("Weather", backref="city")

