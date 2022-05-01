from sqlalchemy import Column, String, JSON
from db.init import Base


class AircraftData(Base):
    __tablename__ = "aircraft_data"

    flight_id = Column(String, primary_key=True, unique=True, index=True)
    data = Column(JSON)

    def __init__(self, flight_id, data):
        self.flight_id = flight_id
        self.data = data
