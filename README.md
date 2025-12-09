# Apollo Engineering Coding Exercise

## Installation and Setup

1. Activate a python virtual environment

```bash
    python3 -m venv venv
    source venv/bin/activate
```

2. Install dependencies

```bash
    pip install -r requirements.txt
```

3. Run the app

```bash
    uvicorn app.app:app --reload
```

## Documentation

- API Docs: Once FastAPI is running, you may optionally view interactive documentation here: `http://localhost:8000/docs`. Easy way to check if setup was successful.

### API

| Method   | Path             | Description                                            | Response Status  |
| -------- | ---------------- | ------------------------------------------------------ | ---------------- |
| `GET`    | `/vehicle`       | Returns all the records in the Vehicle table           | `200 OK`         |
| `GET`    | `/vehicle/{vin}` | Gets the vehicle with the given VIN (case insensitive) | `200 OK`         |
| `POST`   | `/vehicle`       | Creates a new vehicle record                           | `201 Created`    |
| `PUT`    | `/vehicle/{vin}` | Updates an existing vehicle by its VIN                 | `200 OK`         |
| `DELETE` | `/vehicle/{vin}` | Deletes a vehicle by its VIN                           | `204 No Content` |

### Error Handling

| Status Code                | Description                                                                     |
| :------------------------- | :------------------------------------------------------------------------------ |
| `400 Bad Request`          | The server can't parse the request entity as a JSON representation of a Vehicle |
| `422 Unprocessable Entity` | Vvalid JSON, but fails to be validated as a vehicle                             |
| `404 Not Found`            | Vehicle VIN does not exist (in cases of searching/deleting)                     |
| `409 Conflict`             | Vehicle VIN already exists (in cases of creation)                               |

### Testing

```bash
   pytest # or pytest -v to view specific tests
```

### Maintenance

| File                 | Description                                                         |
| -------------------- | ------------------------------------------------------------------- |
| `app/app.py`         | The FastAPI application. Holds all endpoints                        |
| `app/api/models.py`  | Defines Pydantic models for FastAPI request and response validation |
| `app/api/schemas.py` | Defines the Vehicle SQLAlchemy ORM model which maps to the DB       |
| `app/db/`            | DB connection                                                       |
| `tests/`             | Testing suite using pytest                                          |
