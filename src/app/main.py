import typing

from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import torch

from ..exceptions import LanguagePairNotSupportedError
from ..models import (
    CACHE_PATH,
    FINETUNED_PATH,
    FINETUNED_PAIRS,
    PRETRAINED_PAIRS,
)
from ..models.pretrained import load_pretrained_model
from ..models.finetuned import load_finetuned_model

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


@app.get("/")
async def read_root() -> dict[str, str]:
    """API's root message"""
    return {"welcome": "Language Translation API is running"}


@app.post("/predict/", status_code=200)
async def translate_query(
    src_text: str,
    src: typing.Annotated[str, Query(max_length=2)],
    tgt: typing.Annotated[str, Query(max_length=2)],
) -> dict[str, typing.Union[str, int]]:
    """Translates a text from a source language, to a target language"""

    # Check if language pair is supported, and if not raise error
    if (src, tgt) not in FINETUNED_PAIRS + PRETRAINED_PAIRS:
        raise LanguagePairNotSupportedError(src, tgt)

    # Check if model is finetuned
    if (src, tgt) in FINETUNED_PAIRS:
        mt_model = load_finetuned_model(
            language_pair=(src, tgt), finetuned_path=FINETUNED_PATH
        )
    else:
        mt_model = load_pretrained_model(
            language_pair=(src, tgt), cache_path=CACHE_PATH
        )

    tokenizer = mt_model["tokenizer"]
    model = mt_model["model"].to(DEVICE)

    # Translate
    translated = model.generate(
        **tokenizer(src_text, return_tensors="pt", padding=True).to(DEVICE)
    )
    translated_text = [
        tokenizer.decode(t, skip_special_tokens=True) for t in translated
    ]

    response = {
        "status_code": 200,
        "response": f"{translated_text[0]}",
    }

    return response
