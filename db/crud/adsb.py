from sqlalchemy.orm import Session

import db.models.adsb as db_models_adsb


def read_data(db: Session, flight_id: str):
    return (
        db.query(db_models_adsb.AircraftData.data)
        .filter(db_models_adsb.AircraftData.flight_id == flight_id)
        .first()
    )


def create_data(db: Session, data: db_models_adsb.AircraftData, flight_id: str) -> dict:
    db_data = db_models_adsb.AircraftData(flight_id=flight_id, data=data)
    db.add(db_data)
    db.commit()
    return data
