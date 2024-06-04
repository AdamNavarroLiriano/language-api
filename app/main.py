from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch

from .routers import translate
from .exceptions import LanguagePairNotSupportedError

DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

app = FastAPI(title="Language Translation API")

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "*",
    "http://127.0.0.1:8089/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(LanguagePairNotSupportedError)
def language_pair_exception_handler(
    request: Request, exc: LanguagePairNotSupportedError
):
    """Returns LanguagePairNotSupportedError"""
    return JSONResponse(
        status_code=404,
        content={"message": exc.message},
    )


app.include_router(translate.router, prefix="/translate", tags=["translate"])
