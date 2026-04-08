from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppBaseException(Exception):
    def __init__(self, message: str, error_code: str, status_code: int = 400) -> None:
        self.message: str = message
        self.error_code: str = error_code
        self.status_code: int = status_code
        super().__init__(self.message)


unexpected_err_response = JSONResponse(
    status_code=500,
    content={
        "error": "INTERNAL_SERVER_ERROR",
        "message": "Unexpected error occurred.",
    },
)


async def app_exc_handler(_: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, AppBaseException):
        return unexpected_err_response
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.message},
    )


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    if not isinstance(exc, RequestValidationError):
        return unexpected_err_response

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


async def catch_all_handler(_: Request, exc: Exception) -> JSONResponse:
    # TODO: Change to logger
    print(f"[ERROR] Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Something went wrong. Please try again later.",
        },
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(AppBaseException, app_exc_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, catch_all_handler)
