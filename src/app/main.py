from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..exceptions.exceptions import LanguagePairNotSupportedError
from ..models.pretrained import LANGUAGE_PAIRS, PRETRAINED_MODELS

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


def load_pretrained_model(src: str, tgt: str) -> tuple:
    """Loads pretrained models

    :param src: language code for source text
    :type src: str
    :param tgt: language code for target text
    :type tgt: str
    :return: tuple where first element is model object and second element is tokenizer object
    :rtype: tuple
    """
    model_dict = PRETRAINED_MODELS[f"pretrained-{src}-{tgt}"]
    tokenizer = model_dict["tokenizer"]
    model = model_dict["model"]
    return (model, tokenizer)


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
async def translate_query(src_text: str, src: str, tgt: str) -> dict:
    """Translates a text from a source language, to a target language"""
    if (src, tgt) not in LANGUAGE_PAIRS:
        raise LanguagePairNotSupportedError(src, tgt)

    # Load model
    model, tokenizer = load_pretrained_model(src, tgt)

    # Translate
    translated = model.generate(
        **tokenizer(src_text, return_tensors="pt", padding=True)
    )
    translated_text = [
        tokenizer.decode(t, skip_special_tokens=True) for t in translated
    ]

    response = {
        "status_code": 200,
        "response": f"{translated_text[0]}",
    }

    return response
