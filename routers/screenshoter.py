# fmt: off
from winreg import QueryInfoKey
import dependencies
from pydantic import AnyUrl
from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Security,
)
from models import screenshoter
from fastapi.responses import Response
# fmt: on

router = APIRouter()

# Important to include response_class=Response for automatic documentation
@router.post(
    "/screenshot/v1/site/",
    tags=["Screenshoter"],
    response_class=Response,
    # dependencies=[Security(dependencies.get_api_key)],
)
def take_screenshot(
    # site_url: AnyUrl = Query(
    #     ..., description="URL of the site to take a screenshot of"
    # ),  # TODO: `winreg` issue
    site_url: AnyUrl
):
    content = screenshoter.take_screenshot(site_url)
    # content = False
    if content == False:
        raise HTTPException(
            status_code=400, detail=f"Cannot take a screenshot of <{site_url}>"
        )
    else:
        return Response(content=content, media_type="image/png")
