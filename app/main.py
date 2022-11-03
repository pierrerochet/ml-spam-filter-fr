import os
import time

import pickle
import uvicorn
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="API spam filter",
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
        default=5.0,
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
    root = os.path.dirname(os.path.abspath(__file__))
    print(root)
    model_path = os.path.join(root, "ml_models/anti-spam-20221103-121137/model.pkl")
    print(model_path)
    with open(model_path, "rb") as stream:
        app.state.model = pickle.load(stream)


def predict_pred_score(text, strenght):
    proba = app.state.model.predict_proba([text])[0]
    lim = 1 - strenght / 10
    pred = 1 if proba[1] > lim else 0
    score = round(proba[pred], 3)
    return pred, score


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/verify", response_model=Output)
def verify(input: Input = Body(examples=examples)):
    pred, score = predict_pred_score(input.text, input.strength)
    return {
        "is_spam": bool(pred),
        "confidence": score,
        "strength": input.strength,
        "input_text": input.text,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
    }


if __name__ == "__main__":

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
