# fmt: off
from dependencies import *

from db.init import get_db
from sqlalchemy.orm import Session

from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Path,
)
from models import adsb
import db.crud.adsb as db_crud_adsb

# fmt: on

router = APIRouter()


@router.get("/aircraft-data/v0/flight/", include_in_schema=False, deprecated=True)
@router.get(
    "/aircraft-data/v0/flight/{flight_id}",
    response_model=adsb.Data,
    tags=["ADS-B Tracker"],
    dependencies=[Security(get_api_key)],
    deprecated=True,
)
def get_aircraft_data_v0(
    flight_id: adsb.FlightId = Depends(adsb.FlightId),
    # flight_id: str = Path(
    #     ...,
    #     description="6-letter flight number",
    #     example="CKS852",
    #     min_length=2,
    #     max_length=6,
    # )
):
    data = adsb.get_data(flight_id.id)
    if data == False:
        raise HTTPException(
            status_code=404, detail=f"Cannot retreive data for <{flight_id.id}>"
        )
    else:
        return data


@router.get("/aircraft-data/v1/flight/", include_in_schema=False)
@router.get(
    "/aircraft-data/v1/flight/{id}",
    response_model=adsb.Data,
    tags=["ADS-B Tracker"],
    dependencies=[Security(get_api_key)],
)
def get_aircraft_data_v1(
    id: adsb.FlightId = Depends(adsb.FlightId),
    db: Session = Depends(get_db)
    # id: str = Path(
    #     ...,
    #     description="6-letter flight number",
    #     example="CKS852",
    #     min_length=2,
    #     max_length=6,
    # )
):
    db_data = db_crud_adsb.read_data(db, flight_id=id.id)
    if db_data == None:
        data = adsb.get_data_requests(id.id)
        # data = adsb.get_data_requests(id)
        if data == False:
            raise HTTPException(
                status_code=404,
                detail=f"Cannot retreive data for <{id.id}>"
                # status_code=404,
                # detail=f"Cannot retreive data for <{id}>",
            )
        else:
            return db_crud_adsb.create_data(db, flight_id=id.id, data=data)
    else:
        return db_data[0]
