from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import mapped_column, validates
from app.db.db import Base


class Vehicle(Base):
    __tablename__ = "vehicle"

    id = mapped_column(Integer, primary_key=True, index=True)

    vin = mapped_column(String, unique=True, nullable=False)
    manufacturer_name = mapped_column(String, nullable=False)
    description = mapped_column(String, nullable=False)
    horse_power = mapped_column(Integer, nullable=False)
    model_name = mapped_column(String, nullable=False)
    model_year = mapped_column(Integer, nullable=False)
    purchase_price = mapped_column(Float, nullable=False)
    fuel_type = mapped_column(String, nullable=False)

    @validates("vin")
    def uppercase_vin(self, key, vin):
        return vin.upper()
