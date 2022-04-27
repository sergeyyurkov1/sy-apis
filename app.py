# fmt: off
from fastapi import FastAPI
from routers import adsb, test
# fmt: on

app = FastAPI(docs_url="/", redoc_url=None)
# from fastapi.staticfiles import StaticFiles
# app.mount("/", StaticFiles(directory="ui", html=True), name="ui")

import json
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())
    content = {"message": []}  # , "data": None

    for error in exc_json:
        content["message"].append(f'{error["loc"][-1]}: {error["msg"]}')

    return JSONResponse(content=content, status_code=400)  # 422


app.include_router(
    adsb.router,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {"id": "bar", "value": "The bar tenders"}
                }
            },
        }
    },
)
app.include_router(test.router)

# from fastapi.openapi.utils import get_openapi
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title=app.title,
#         version=app.version,
#         description=app.description,
#         routes=app.routes,
#     )
#     methods = ["post", "get", "put", "delete"]
#     for path in openapi_schema["paths"]:
#         for method in methods:
#             try:
#                 del openapi_schema["paths"][path][method]["responses"]["422"]
#             except KeyError:
#                 pass
# for schema in list(openapi_schema["components"]["schemas"]):
#     if schema == "HTTPValidationError" or schema == "ValidationError":
#         del openapi_schema["components"]["schemas"][schema]
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi
