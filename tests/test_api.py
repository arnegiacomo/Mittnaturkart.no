#!/usr/bin/env python3
import requests
import time
import sys
import os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")

def wait_for_api(max_retries=30):
    print("Waiting for API to be ready...")
    for i in range(max_retries):
        try:
            response = requests.get(f"{API_URL}/health", timeout=2)
            if response.status_code == 200:
                print(f"✓ API is ready after {i+1} attempts")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)
    print("✗ API failed to start")
    return False

def test_nginx_proxy():
    print("\n--- Testing Nginx Reverse Proxy ---")

    # Test frontend is served at root
    response = requests.get(f"{API_URL}/")
    assert response.status_code == 200, f"Root endpoint failed: {response.status_code}"
    assert "text/html" in response.headers.get("Content-Type", ""), "Root should return HTML"
    print("✓ Frontend accessible at root")

    # Test that API docs works
    response = requests.get(f"{API_URL}/docs")
    assert response.status_code == 200, f"Docs endpoint failed: {response.status_code}"
    print("✓ API docs endpoint accessible")

    # Verify API endpoints work through nginx
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200, "Health check through nginx failed"
    data = response.json()
    assert data["status"] == "ok"
    print("✓ Nginx is properly proxying API requests")

def test_health_check():
    print("\n--- Testing Health Check ---")
    response = requests.get(f"{API_URL}/health")
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    assert response.json()["status"] == "ok"
    print("✓ Health check passed")

def test_create_observation():
    print("\n--- Testing Create Observation ---")
    observation = {
        "species": "Rødstrupe",
        "date": datetime.now().isoformat(),
        "latitude": 59.9139,
        "longitude": 10.7522,
        "notes": "Test observation",
        "category": "Fugl"
    }
    response = requests.post(f"{API_URL}/api/v1/observations", json=observation)
    assert response.status_code == 201, f"Create failed: {response.status_code} - {response.text}"
    data = response.json()
    assert data["species"] == observation["species"]
    assert data["category"] == observation["category"]
    assert "id" in data
    print(f"✓ Created observation with ID: {data['id']}")
    return data["id"]

def test_get_all_observations():
    print("\n--- Testing Get All Observations ---")
    response = requests.get(f"{API_URL}/api/v1/observations")
    assert response.status_code == 200, f"Get all failed: {response.status_code}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    print(f"✓ Retrieved {len(data)} observation(s)")
    return data

def test_get_observation(observation_id):
    print("\n--- Testing Get Single Observation ---")
    response = requests.get(f"{API_URL}/api/v1/observations/{observation_id}")
    assert response.status_code == 200, f"Get single failed: {response.status_code}"
    data = response.json()
    assert data["id"] == observation_id
    print(f"✓ Retrieved observation ID: {observation_id}")
    return data

def test_update_observation(observation_id):
    print("\n--- Testing Update Observation ---")
    update_data = {
        "notes": "Updated test observation"
    }
    response = requests.put(f"{API_URL}/api/v1/observations/{observation_id}", json=update_data)
    assert response.status_code == 200, f"Update failed: {response.status_code}"
    data = response.json()
    assert data["notes"] == update_data["notes"]
    print(f"✓ Updated observation ID: {observation_id}")

def test_delete_observation(observation_id):
    print("\n--- Testing Delete Observation ---")
    response = requests.delete(f"{API_URL}/api/v1/observations/{observation_id}")
    assert response.status_code == 204, f"Delete failed: {response.status_code}"

    # Verify deletion
    response = requests.get(f"{API_URL}/api/v1/observations/{observation_id}")
    assert response.status_code == 404, "Observation should not exist after deletion"
    print(f"✓ Deleted observation ID: {observation_id}")

def run_tests():
    print("=" * 50)
    print("Starting API Tests (via Nginx)")
    print("=" * 50)

    if not wait_for_api():
        sys.exit(1)

    try:
        test_nginx_proxy()
        test_health_check()
        observation_id = test_create_observation()
        test_get_all_observations()
        test_get_observation(observation_id)
        test_update_observation(observation_id)
        test_delete_observation(observation_id)

        print("\n" + "=" * 50)
        print("✓ All tests passed!")
        print("=" * 50)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
