from fastapi import status

CAR_1 = {
    "manufacturer_name": "Manufacturer 1",
    "description": "Description 1",
    "horse_power": 500,
    "model_name": "Model 1",
    "model_year": 2025,
    "purchase_price": 32000.01,
    "fuel_type": "Fuel Type 1",
    "vin": "1234567890ABCDEFG",
}

CAR_2 = {
    "manufacturer_name": "Manufacturer 2",
    "description": "Description 2",
    "horse_power": 300,
    "model_name": "Model 2",
    "model_year": 2000,
    "purchase_price": 12000.00,
    "fuel_type": "Fuel Type 2",
    "vin": "AAAAAAAAAAAAAAAAA",
}


def test_create_vehicle_success(client):
    """POST /vehicle (201 Created)"""

    first_car = client.post("/vehicle", json=CAR_1)
    assert first_car.status_code == status.HTTP_201_CREATED
    data = first_car.json()
    for key, val in CAR_1.items():
        assert data[key] == val

    second_car = client.post("/vehicle", json=CAR_2)
    assert second_car.status_code == status.HTTP_201_CREATED
    data = second_car.json()
    for key, val in CAR_2.items():
        assert data[key] == val


def test_create_vehicle_duplicate_vin(client):
    """POST /vehicle (409 Duplicate VIN)"""

    response = client.post("/vehicle", json=CAR_1)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"]


def test_create_vehicle_bad_request(client):
    """POST /vehicle (400 Bad Request)"""

    invalid_data = "new vehicle"

    response = client.post("/vehicle", json=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_vehicle_by_vin_bad_request(client):
    """PUT /vehicle/{vin} (400 Bad Request)"""

    invalid_data = "new vehicle"

    response = client.put(f"/vehicle/{CAR_1['vin']}", json=invalid_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_vehicle_unprocessable(client):
    """POST /vehicle (422 Unprocessable Entity)"""

    invalid_data = CAR_1.copy()
    invalid_data["model_year"] = "last year"

    response = client.post("/vehicle", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    invalid_data = {"company": "Apollo Global Management", "intern": "Daniel"}
    response = client.post("/vehicle", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_get_vehicle_by_vin_success(client):
    """GET /vehicle/{vin} (200 OK)"""

    lower_case_search = client.get(f"/vehicle/{CAR_1['vin'].lower()}")
    assert lower_case_search.status_code == status.HTTP_200_OK
    assert lower_case_search.json()["vin"] == CAR_1["vin"]

    upper_case_search = client.get(f"/vehicle/{CAR_1['vin'].upper()}")
    assert upper_case_search.status_code == status.HTTP_200_OK
    assert upper_case_search.json()["vin"] == CAR_1["vin"]

    normal_search = client.get(f"/vehicle/{CAR_1['vin']}")
    assert normal_search.status_code == status.HTTP_200_OK
    assert normal_search.json()["vin"] == CAR_1["vin"]


def test_get_vehicle_by_vin_not_found(client):
    """GET /vehicle/{vin} (404 Not Found)"""

    response = client.get("/vehicle/does_not_exist")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Unknown VIN"


def test_get_all_vehicles_success(client):
    """GET /vehicle (200 OK)"""

    response = client.get("/vehicle")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 2
    assert any(v["vin"] == CAR_1["vin"] for v in response.json())
    assert any(v["vin"] == CAR_2["vin"] for v in response.json())


def test_update_vehicle_success(client):
    """PUT /vehicle/{vin} (200 OK)"""
    updated_data = {
        **CAR_1,
        "purchase_price": 999999.99,
    }

    response = client.put(f"/vehicle/{CAR_1['vin']}", json=updated_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["purchase_price"] == 999999.99
    assert data["vin"] == CAR_1["vin"]


def test_update_vehicle_not_found(client):
    """PUT /vehicle/{vin} (404 Not Found)"""

    response = client.put("/vehicle/NONEXISTENTVIN", json=CAR_1)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Unknown VIN"


def test_delete_vehicle_success(client):
    """DELETE /vehicle/{vin} (204 No Content)"""

    response = client.delete(f"/vehicle/{CAR_1['vin']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content

    response = client.get(f"/vehicle/{CAR_1['vin']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_populate_table(client):
    CARS = [
        {
            "manufacturer_name": "Honda",
            "description": "Mid-sized family sedan",
            "horse_power": 190,
            "model_name": "Accord",
            "model_year": 2024,
            "purchase_price": 28500.00,
            "fuel_type": "Gasoline",
            "vin": "JHMBY5G65R0100001",
        },
        {
            "manufacturer_name": "BMW",
            "description": "Luxury sports coupe",
            "horse_power": 382,
            "model_name": "M440i",
            "model_year": 2023,
            "purchase_price": 58900.00,
            "fuel_type": "Premium Gasoline",
            "vin": "WBAF9C0C3N7987654",
        },
        {
            "manufacturer_name": "Nissan",
            "description": "Compact electric crossover",
            "horse_power": 214,
            "model_name": "Ariya",
            "model_year": 2025,
            "purchase_price": 43500.00,
            "fuel_type": "Electric",
            "vin": "JN1AZ00E8R0000001",
        },
        {
            "manufacturer_name": "Ram",
            "description": "Heavy-duty pickup truck",
            "horse_power": 410,
            "model_name": "2500",
            "model_year": 2022,
            "purchase_price": 65000.00,
            "fuel_type": "Diesel",
            "vin": "3C6RRCAG1N1543210",
        },
        {
            "manufacturer_name": "Subaru",
            "description": "All-wheel drive wagon",
            "horse_power": 260,
            "model_name": "Outback XT",
            "model_year": 2024,
            "purchase_price": 37995.00,
            "fuel_type": "Gasoline",
            "vin": "4S4BHAFB1R0888888",
        },
    ]

    for car in CARS:
        response = client.post("/vehicle", json=car)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        for key, val in car.items():
            assert data[key] == val
