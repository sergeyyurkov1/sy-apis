# fmt: off
from fastapi import FastAPI
from routers import adsb, test, screenshoter
# fmt: on

app = FastAPI(docs_url="/", redoc_url=None)
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

import json
from fastapi.exceptions import (
    RequestValidationError,
    ValidationError,
)
from fastapi.responses import JSONResponse


# @app.exception_handler(RequestValidationError)
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request, exc):
#     exc_json = json.loads(exc.json())

#     print(exc_json)

#     content = {"detail": []}

#     for e, error in enumerate(exc_json):
#         content["detail"].append(
#             {"loc": [error["loc"][e], e], "msg": error["msg"], "type": error["type"]}
#         )

#     return JSONResponse(content=content, status_code=422)  # 400


app.include_router(
    adsb.router,
    responses={
        # 400: {
        #     "content": {"application/json": {}},
        #     "description": "Bad Request",
        #     # "content": {"application/json": {"example": {}}},
        # },
        200: {
            "description": "OK",
            "content": {"application/json": {}},
        },
        404: {
            "description": "Flight Not Found",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
        },
    },
)
app.include_router(test.router)
app.include_router(
    screenshoter.router,
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "OK",
        },
        400: {
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPValidationError"}
                }
            },
            "description": "",
        },
    },
)

from fastapi.openapi.utils import get_openapi


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SY's collection of APIs",
        version="1.0.1",
        description="Serve as endpoints for my projects",
        routes=app.routes,
    )

    # methods = ["post", "get", "put", "delete"]
    # for path in openapi_schema["paths"]:
    #     for method in methods:
    #         try:
    #             del openapi_schema["paths"][path][method]["responses"]["422"]
    #         except KeyError:
    #             pass

    # for schema in list(openapi_schema["components"]["schemas"]):
    #     if schema == "HTTPValidationError" or schema == "ValidationError":
    #         del openapi_schema["components"]["schemas"][schema]

    for schema in list(openapi_schema["components"]["schemas"]):
        if schema == "ValidationError":
            del openapi_schema["components"]["schemas"][schema]

        if schema == "HTTPValidationError":
            openapi_schema["components"]["schemas"][schema] = {
                # "title": "ValidationError",
                "required": ["detail"],
                "type": "object",
                "properties": {"detail": {"title": "Detail", "type": "string"}},
            }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
