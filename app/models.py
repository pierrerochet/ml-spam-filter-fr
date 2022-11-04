from pydantic import BaseModel, Field


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
