from sqlalchemy.orm import Session

from db import models as db_models


def read_data(db: Session, flight_id: str):
    return (
        db.query(db_models.AircraftData.data)
        .filter(db_models.AircraftData.flight_id == flight_id)
        .first()
    )


def create_data(db: Session, data: db_models.AircraftData, flight_id: str):
    db_data = db_models.AircraftData(flight_id=flight_id, data=data)
    db.add(db_data)
    db.commit()
    return data
