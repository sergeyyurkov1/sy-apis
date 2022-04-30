# fmt: off
import dependencies
from pydantic import AnyUrl
from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Security,
)
from fastapi.security.api_key import APIKey
from models import screenshoter
from fastapi.responses import Response
# fmt: on

router = APIRouter()

# Important to include response_class=Response for automatic documentation
@router.post(
    "/screenshoter/v1/screenshot/",
    tags=["Screenshoter"],
    response_class=Response,
    dependencies=[Security(dependencies.get_api_key)],
)
def get_screenshot(
    site_url: AnyUrl,
):
    content = screenshoter.get_screenshot(site_url)
    content = False
    if content == False:
        raise HTTPException(
            status_code=400, detail="Cannot take a screenshot of the URL."
        )
    else:
        return Response(content=content, media_type="image/png")
