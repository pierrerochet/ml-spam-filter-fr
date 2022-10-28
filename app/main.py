import time

import joblib
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI(
    title="API anti-spam",
    description="Checks if an email is spam using its textual content",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)


class Input(BaseModel):
    text: str = Field(title="Textual content from email")
    strength: float = Field(
        title="Strength to apply to the filter",
        default=0.5,
        ge=0.0,
        le=10.0,
    )


class Output(BaseModel):
    is_spam: bool
    strength: float
    confidence: float
    input_text: str
    time: str


examples = {
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


@app.on_event("startup")
async def startup_event():
    model_path = "./app/ml_models/anti-spam-20221025-141032/model.joblib"
    app.state.model = joblib.load(model_path)


def predict_pred_score(text, strenght):
    proba = app.state.model.predict_proba([text])[0]
    lim = 1 - strenght / 10
    pred = 1 if proba[1] > lim else 0
    score = round(proba[pred], 3)
    return pred, score


@app.post("/verify", response_model=Output)
def read_root(input: Input = Body(examples=examples)):
    pred, score = predict_pred_score(input.text, input.strength)
    return {
        "is_spam": bool(pred),
        "confidence": score,
        "strength": input.strength,
        "input_text": input.text,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    }
