from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.services.reco import get_recommendation_for_field
from app.schemas.reco import RecommendationOut
from app.services import voice as voice_service
from sqlalchemy import text

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/recommendations/{field_id}", response_model=RecommendationOut)
def get_reco(field_id: int, db: Session = Depends(get_db)):
    return get_recommendation_for_field(field_id)

@router.post("/voice/asr")
async def asr(audio: UploadFile = File(...)):
    data = await audio.read()
    result = voice_service.speech_to_text(data, language="hi-IN")
    return {"text": result.text, "confidence": result.confidence}

@router.post("/voice/tts")
async def tts(payload: dict):
    text_in = payload.get("text", "नमस्ते किसान भाई!")
    b64 = voice_service.text_to_speech(text_in, language="hi-IN")
    return {"audio_b64": b64}

@router.post("/advisories")
def create_advisory(payload: dict, db: Session = Depends(get_db)):
    farmer_id = payload.get("farmer_id")
    field_id = payload.get("field_id")
    crop_id = payload.get("crop_id")
    text_value = payload.get("text", "")
    audio_url = payload.get("audio_url")
    q = text("""
        INSERT INTO advisories (farmer_id, field_id, crop_id, text, audio_url)
        VALUES (:farmer_id, :field_id, :crop_id, :text_value, :audio_url)
        RETURNING id
    """)
    new_id = db.execute(q, dict(farmer_id=farmer_id, field_id=field_id, crop_id=crop_id,
                                text_value=text_value, audio_url=audio_url)).scalar_one()
    db.commit()
    return {"id": new_id}

@router.get("/advisories/{farmer_id}")
def list_advisories(farmer_id: int, db: Session = Depends(get_db)):
    q = text("SELECT id, field_id, crop_id, text, audio_url, created_at FROM advisories WHERE farmer_id = :fid ORDER BY created_at DESC")
    rows = db.execute(q, dict(fid=farmer_id)).mappings().all()
    return {"items": [dict(r) for r in rows]}

@router.post("/feedback")
def create_feedback(payload: dict, db: Session = Depends(get_db)):
    farmer_id = payload.get("farmer_id")
    advisory_id = payload.get("advisory_id")
    rating = payload.get("rating", 5)
    comment = payload.get("comment")
    q = text("""
        INSERT INTO feedback (farmer_id, advisory_id, rating, comment)
        VALUES (:farmer_id, :advisory_id, :rating, :comment)
        RETURNING id
    """)
    new_id = db.execute(q, dict(farmer_id=farmer_id, advisory_id=advisory_id, rating=rating, comment=comment)).scalar_one()
    db.commit()
    return {"id": new_id}
