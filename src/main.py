from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.auth.router import router as auth_router
from src.exceptions import AppBaseException


app = FastAPI()
app.include_router(auth_router)


@app.exception_handler(AppBaseException)
async def app_exc_handler(_: Request, exc: AppBaseException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        loc = error.get("loc", [])
        field = str(loc[-1]) if loc else "unknown"

        formatted_errors.append(
            {
                "field": field,
                "message": error.get("msg", "Invalid value"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "VALIDATION_ERROR",
            "message": "Invalid input data provided.",
            "details": formatted_errors,
        },
    )


@app.exception_handler(Exception)
async def catch_all_handler(_: Request, exc: Exception):
    print(f"[ERROR] Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Something went wrong. Please try again later.",
        },
    )
