# fmt: off
from dependencies import *

from typing import List
from fastapi import (
    APIRouter,
)
# fmt: on

router = APIRouter()
@router.get("/test/v1/", tags=["test"])
def data():
    return {
        "test": "a",
    }