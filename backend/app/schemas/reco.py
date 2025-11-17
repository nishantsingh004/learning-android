from pydantic import BaseModel

class CropScore(BaseModel):
    crop_id: int
    name_en: str
    name_hi: str
    profit_per_acre: float
    demand_score: int
    risk_score: int
    try_acre_pct: int = 20

class RecommendationOut(BaseModel):
    field_id: int
    top1: CropScore
    top2: CropScore
    top3: CropScore
    confidence: float
    explanation: str | None = None
