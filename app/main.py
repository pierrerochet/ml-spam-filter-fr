import os
import pickle

import uvicorn
from fastapi import Body, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from models import Input, Output
from utils import predict_pred_score

app = FastAPI(
    title="API spam filter",
    description="Checks if an email is spam using its textual content",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    root = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(root, "ml_models/spam-filter-latest/model.pkl")
    with open(model_path, "rb") as stream:
        app.state.model = pickle.load(stream)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


@app.post("/check_email", response_model=Output)
def check_email(
    input: Input = Body(
        examples={
            "spam": {
                "summary": "Spam example",
                "description": "A text from a spam email",
                "value": {
                    "text": "Vous avez gagnez un cadeau ! Recevez votre gain en cliquant ici !"
                },
            },
            "legit": {
                "summary": "Legit example",
                "description": "A text from a legit email",
                "value": {"text": "La réunion aura lieu demain à 14h"},
            },
        }
    )
):
    return predict_pred_score(app.state.model, input.text, input.strength)


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
