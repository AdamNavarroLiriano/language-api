from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ..models.pretrained import PRETRAINED_MODELS

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
    model_dict = PRETRAINED_MODELS[f"pretrained-{src}-{tgt}"]
    tokenizer = model_dict["tokenizer"]
    model = model_dict["model"]
    return (model, tokenizer)


@app.get("/")
async def read_root():
    return {"welcome": "Language Translation API is running"}


@app.post("/predict/", status_code=200)
async def translate_query(src_text: str, src: str, tgt: str):
    # Load model
    model, tokenizer = load_pretrained_model(src, tgt)

    # Translate
    translated = model.generate(
        **tokenizer(src_text, return_tensors="pt", padding=True)
    )
    translated_text = [
        tokenizer.decode(t, skip_special_tokens=True) for t in translated
    ]

    return (
        {
            "status_code": 200,
            "response": f"{translated_text[0]}",
        },
    )
