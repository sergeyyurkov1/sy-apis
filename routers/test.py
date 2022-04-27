# fmt: off
from dependencies import *

from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security.api_key import APIKey
# fmt: on

router = APIRouter()
@router.get("/test/v1/", tags=["test"])
def data(api_key: APIKey = Depends(get_api_key)):
    return {
        "test": "a",
    }