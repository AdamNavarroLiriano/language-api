from fastapi import APIRouter, Query
import typing
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

router = APIRouter()


@router.get("/")
async def read_root() -> dict[str, str]:
    """API's root message"""
    return {"welcome": "Language Translation API is running"}


@router.post("/sentence/", status_code=200)
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
