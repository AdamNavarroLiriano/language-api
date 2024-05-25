from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/")
async def read_root():
    return {"welcome": "Language Translation API is running"}


@app.post("/predict/", status_code=200)
async def translate_query(request: str):

    return (
        {
            "status_code": 200,
            "response": f"This is a placeholder response for {request}",
        },
    )
