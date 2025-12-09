from pydantic import BaseModel, Field, ConfigDict


# base Vehicle
# these fields can be modified
class Vehicle(BaseModel):
    manufacturer_name: str = Field(...)
    description: str = Field(...)
    horse_power: int = Field(..., ge=0)
    model_name: str = Field(...)
    model_year: int = Field(..., ge=1886)
    purchase_price: float = Field(..., ge=0.0)
    fuel_type: str = Field(...)


# POST /vehicle
# VIN is required when creating a Vehicle
class VehicleCreate(Vehicle):
    vin: str = Field(...)


class VehicleResponse(Vehicle):
    vin: str = Field(...)
    id: int = Field(...)

    model_config = ConfigDict(from_attributes=True)
