from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Numeric, Date
from sqlalchemy.sql import func
from geoalchemy2 import Geography
from app.db.session import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True)
    role = Column(String(20), nullable=False, default="farmer")
    locale = Column(String(10), default="hi-IN")
    created_at = Column(DateTime, server_default=func.now())

class Farmer(Base):
    __tablename__ = "farmers"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(Text)
    village = Column(Text)
    district = Column(Text)
    state = Column(Text)
    lat = Column(Numeric)
    lon = Column(Numeric)
    created_at = Column(DateTime, server_default=func.now())

class Field(Base):
    __tablename__ = "fields"
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id", ondelete="CASCADE"))
    area_acres = Column(Numeric(8,2))
    soil_type = Column(Text)
    irrigation = Column(Text)
    geom = Column(Geography("POLYGON", 4326))

class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True)
    name_en = Column(Text)
    name_hi = Column(Text)
    category = Column(Text)

class CropPrice(Base):
    __tablename__ = "crop_prices"
    id = Column(Integer, primary_key=True)
    crop_id = Column(Integer, ForeignKey("crops.id"))
    mandi = Column(Text)
    price_per_quintal = Column(Numeric(10,2))
    price_date = Column(Date)

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    created_at = Column(DateTime, server_default=func.now())
    top1_crop_id = Column(Integer, ForeignKey("crops.id"))
    top1_profit = Column(Numeric(12,2))
    top1_demand_score = Column(Integer)
    top1_risk_score = Column(Integer)
    top2_crop_id = Column(Integer, ForeignKey("crops.id"))
    top2_profit = Column(Numeric(12,2))
    top2_demand_score = Column(Integer)
    top2_risk_score = Column(Integer)
    top3_crop_id = Column(Integer, ForeignKey("crops.id"))
    top3_profit = Column(Numeric(12,2))
    top3_demand_score = Column(Integer)
    top3_risk_score = Column(Integer)
    details = Column(JSON)

class Advisory(Base):
    __tablename__ = "advisories"
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id", ondelete="CASCADE"))
    field_id = Column(Integer, ForeignKey("fields.id", ondelete="CASCADE"))
    crop_id = Column(Integer, ForeignKey("crops.id"))
    text = Column(Text)
    audio_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    advisory_id = Column(Integer, ForeignKey("advisories.id"))
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
