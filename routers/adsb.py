# fmt: off
from dependencies import *

from typing import List
from fastapi import (
    APIRouter,
    Depends,
    Path
)
from fastapi.security.api_key import APIKey
from models import adsb
# fmt: on

router = APIRouter()


@router.get("/adsb/v0/flight/", include_in_schema=False)
@router.get("/adsb/v0/flight/{id}", response_model=adsb.Data, tags=["flight_data"])
def data(
    id: adsb.Id = Depends(), api_key: APIKey = Depends(get_api_key)
):  # id: str = Path(..., min_length=1)
    data = adsb.get_data(id.id)
    if data == False:
        raise HTTPException(status_code=404)
    else:
        return data


@router.get("/adsb/v1/flight/", include_in_schema=False)
@router.get(
    "/adsb/v1/flight/{id}", response_model=adsb.Data, tags=["flight_data"]
)  # response_model=adsb.Data,
def get_data_requests(
    id: adsb.Id = Depends(),
):  # id: str = Path(..., min_length=1), api_key: APIKey = Depends(get_api_key)
    data = adsb.get_data_requests(id.id)
    if data == False:
        raise HTTPException(status_code=404)
    else:
        return data
