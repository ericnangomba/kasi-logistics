import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
VALID_TOKEN = "default-dev-token-change-me"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data

def test_route_optimization_unauthorized():
    response = client.post("/v1/routes/optimize", json={
        "depot_coordinates": [-33.95, 18.54],
        "stops": []
    })
    assert response.status_code == 401

def test_route_optimization_success():
    headers = {"Authorization": f"Bearer {VALID_TOKEN}"}
    payload = {
        "depot_coordinates": [-33.9500, 18.5400],
        "max_vehicle_capacity_kg": 500.0,
        "stops": [
            {
                "stop_id": "stop_1",
                "node_id": "node_001",
                "merchant_name": "Mama Africa Spaza",
                "order_volume_kg": 150.0,
                "coordinates": [-33.9512, 18.5431]
            }
        ]
    }
    response = client.post("/v1/routes/optimize", headers=headers, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "total_distance_km" in data
    assert "ordered_stops" in data
    assert len(data["ordered_stops"]) == 1
    assert data["vehicle_load_utilized_percentage"] == 30.0

