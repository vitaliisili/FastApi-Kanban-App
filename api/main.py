from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from api.controller import user_controller, role_controller
from api.exception.exception_handler import validation_exception_handler


app = FastAPI()
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.include_router(user_controller.router)
app.include_router(role_controller.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def hello():
    return "Hack NASA with HTML only"
