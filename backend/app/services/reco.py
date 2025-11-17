from app.schemas.reco import RecommendationOut, CropScore

def get_recommendation_for_field(field_id: int) -> RecommendationOut:
    top1 = CropScore(crop_id=1, name_en="Mustard", name_hi="सरसों",
                     profit_per_acre=56500, demand_score=82, risk_score=12)
    top2 = CropScore(crop_id=2, name_en="Wheat", name_hi="गेहूँ",
                     profit_per_acre=50200, demand_score=75, risk_score=15)
    top3 = CropScore(crop_id=3, name_en="Pulses", name_hi="दालें",
                     profit_per_acre=44300, demand_score=68, risk_score=28)
    return RecommendationOut(
        field_id=field_id,
        top1=top1, top2=top2, top3=top3,
        confidence=0.78,
        explanation="Based on rainfall deviation, loam soil, and Ambala mandi prices."
    )
