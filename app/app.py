from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.api import models, schemas
from app.db.db import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get(
    "/vehicle",
    response_model=list[schemas.VehicleResponse],
    status_code=status.HTTP_200_OK,
)
def get_vehicles(db=Depends(get_db)):
    """Returns all the records in the Vehicle table"""
    return db.query(models.Vehicle).all()


@app.get(
    "/vehicle/{vin}",
    response_model=schemas.VehicleResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Unknown VIN"}},
)
def get_vehicle_by_vin(vin: str, db=Depends(get_db)):
    """Gets the vehicle with the given VIN"""
    db_vehicle = (
        db.query(models.Vehicle).filter(models.Vehicle.vin == vin.upper()).first()
    )
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown VIN")

    return db_vehicle


@app.post(
    "/vehicle",
    response_model=schemas.VehicleResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"description": "Bad Request"},
        409: {"description": "Duplicate VIN"},
        422: {"description": "Unprocessable Entity"},
    },
)
async def post_vehicle(request: Request, db=Depends(get_db)):
    """Creates a new vehicle record"""

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad Request",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON: expected object",
        )

    try:
        vehicle = schemas.VehicleCreate(**body)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ERROR: {e.errors()}",
        )

    # converts Pydantic model to ORM model
    db_vehicle = models.Vehicle(**vehicle.model_dump())

    try:
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Vehicle with VIN {vehicle.vin.upper()} already exists",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR: {str(e)}",
        )


@app.put(
    "/vehicle/{vin}",
    response_model=schemas.VehicleResponse,
    status_code=status.HTTP_200_OK,
    responses={404: {"description": "Unknown VIN"}},
)
async def update_vehicle(vin: str, request: Request, db=Depends(get_db)):
    """Updates an existing vehicle by its VIN"""

    try:
        body = await request.json()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON",
        )

    if not isinstance(body, dict):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid JSON",
        )

    try:
        data = schemas.Vehicle(**body)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"ERROR: {e.errors()}",
        )

    # checks if vehicle exists
    db_vehicle = (
        db.query(models.Vehicle).filter(models.Vehicle.vin == vin.upper()).first()
    )
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown VIN")

    update_data = data.model_dump()
    for key, value in update_data.items():
        setattr(db_vehicle, key, value)

    try:
        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)

        return db_vehicle
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR: {str(e)}",
        )


@app.delete(
    "/vehicle/{vin}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "No Content"},
        404: {"description": "Unknown VIN"},
    },
)
def delete_vehicle(vin: str, db: Session = Depends(get_db)):
    """Deletes a vehicle by its VIN"""

    # checks if vehicle exists
    db_vehicle = (
        db.query(models.Vehicle).filter(models.Vehicle.vin == vin.upper()).first()
    )
    if not db_vehicle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown VIN")

    try:
        db.delete(db_vehicle)
        db.commit()
        return

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ERROR: {str(e)}",
        )
