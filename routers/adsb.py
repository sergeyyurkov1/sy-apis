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
    "/aircraft-data/v0/flight/{flight}",
    response_model=adsb.Data,
    tags=["ADS-B Tracker"],
    dependencies=[Security(get_api_key)],
    deprecated=True,
)
def get_aircraft_data_v0(
    flight: adsb.Flight = Depends(adsb.Flight),
    # flight: str = Path(
    #     ...,
    #     description="6-letter flight number",
    #     example="CKS852",
    #     min_length=2,
    #     max_length=6,
    # )
):
    data = adsb.get_data(flight.id)
    if data == False:
        raise HTTPException(
            status_code=404, detail=f"Cannot retreive data for <{flight.id}>"
        )
    else:
        return data


@router.get("/aircraft-data/v1/flight/", include_in_schema=False)
@router.get(
    "/aircraft-data/v1/flight/{flight}",
    response_model=adsb.Data,
    tags=["ADS-B Tracker"],
    dependencies=[Security(get_api_key)],
)
def get_aircraft_data_v1(
    flight: adsb.Flight = Depends(adsb.Flight),
    db: Session = Depends(get_db)
    # flight: str = Path(
    #     ...,
    #     description="6-letter flight number",
    #     example="CKS852",
    #     min_length=2,
    #     max_length=6,
    # )
):
    db_data = db_crud_adsb.read_data(db, flight_id=flight.id)
    if db_data == None:
        data = adsb.get_data_requests(flight.id)
        # data = adsb.get_data_requests(id)
        if data == False:
            raise HTTPException(
                status_code=404,
                detail=f"Cannot retreive data for <{flight.id}>"
                # status_code=404,
                # detail=f"Cannot retreive data for <{id}>",
            )
        else:
            return db_crud_adsb.create_data(db, flight_id=flight.id, data=data)
    else:
        return db_data[0]


responses = {
    200: {
        "description": "",
        "content": {
            "application/json": {"schema": {"$ref": "#/components/schemas/FullData"}}
        },
    },
}


@router.get("/aircraft-data/v1/flight/", include_in_schema=False)
@router.get(
    "/aircraft-data/v1/flight/{flight}/full",
    tags=["ADS-B Tracker"],
    dependencies=[Security(get_api_key)],
    responses=responses,
)
def get_aircraft_data_v1_full(
    flight: adsb.Flight = Depends(adsb.Flight),
    # db: Session = Depends(get_db)
    # flight: str = Path(
    #     ...,
    #     description="6-letter flight number",
    #     example="CKS852",
    #     min_length=2,
    #     max_length=6,
    # )
):
    data = adsb.get_data_requests(flight.id, full=True)
    if data == False:
        raise HTTPException(
            status_code=404, detail=f"Cannot retreive data for <{flight.id}>"
        )
    else:
        return data
