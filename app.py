# fmt: off
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import (
    RequestValidationError,
    # ValidationError,
)
from fastapi.responses import JSONResponse

import json

from routers import (
    adsb,
    screenshoter,
)
from db.init import engine, Base
# fmt: on

app = FastAPI(docs_url="/", redoc_url=None)
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

Base.metadata.create_all(bind=engine)


# @app.exception_handler(ValidationError)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())

    # import logging

    # logging.basicConfig(
    #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #     # level=logging.INFO,
    #     level=logging.DEBUG,
    # )

    # logger = logging.getLogger()
    # logger.debug(exc_json)

    # print(exc_json)

    # content = {"detail": []}  # message
    # for e, error in enumerate(exc_json):
    #     content["detail"].append(
    #         {"loc": [error["loc"][e], e], "msg": error["msg"], "type": error["type"]}
    #     )

    # content = {"message": []}  # message
    # for e, error in enumerate(exc_json):
    #     content["message"].append(
    #         {"loc": [error["loc"][e], e], "msg": error["msg"], "type": error["type"]}
    #     )

    # content = {"detail": exc.errors()}

    content = {"detail": f'{exc_json[-1]["loc"][-1]}: {exc_json[-1]["msg"]}'}

    return JSONResponse(content=content, status_code=422)  # 400


app.include_router(
    adsb.router,
    responses={
        200: {
            "description": "",
            "content": {"application/json": {}},
        },
        # 400: {
        #     "description": "Bad Request",
        #     "content": {"application/json": {}},
        # },
        404: {
            "description": "Not Found Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
            },
        },
        422: {
            "description": "Unprocessable Entity Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
            },
        },
    },
)
app.include_router(
    screenshoter.router,
    responses={
        200: {
            "description": "",
            "content": {"image/png": {}},
        },
        400: {
            "description": "Bad Request Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
            },
        },
        422: {
            "description": "Unprocessable Entity Error",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Error"}}
            },
        },
    },
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="SY's collection of APIs",
        version="1.1.1",
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
        if schema == "ValidationError" or schema == "HTTPValidationError":
            del openapi_schema["components"]["schemas"][schema]

        openapi_schema["components"]["schemas"]["Error"] = {
            "title": "Error",
            "required": ["detail"],
            "type": "object",
            "properties": {"detail": {"title": "Error message", "type": "string"}},
        }

        openapi_schema["components"]["schemas"]["FullData"] = {
            "title": "FullData",
            # "required": ["detail"],
            "type": "object",
            # "properties": {"detail": {"title": "Error message", "type": "string"}},
        }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
