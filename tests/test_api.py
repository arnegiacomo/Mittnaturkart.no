#!/usr/bin/env python3
import requests
import time
import sys
import os
from datetime import datetime

API_URL = os.getenv("API_URL", "http://localhost:8000")
HEADERS = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2IiwiZW1haWwiOiIxMjNAMTIzLmNvbSIsImV4cCI6MTc2Njk1Nzk3M30.Gf2rRY-Ur6BhC16dE9E6iwrXz_Cm3z8EtS6vfcQeOTM"}

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

def test_create_location():
    print("\n--- Testing Create Location ---")
    location = {
        "name": "Test Location",
        "latitude": 59.9139,
        "longitude": 10.7522,
        "description": "A test location in Oslo",
        "address": "Oslo, Norway"
    }
    response = requests.post(f"{API_URL}/api/v1/locations", json=location, headers=HEADERS)
    assert response.status_code == 201, f"Create failed: {response.status_code} - {response.text}"
    data = response.json()
    assert data["name"] == location["name"]
    assert data["latitude"] == location["latitude"]
    assert data["longitude"] == location["longitude"]
    assert "id" in data
    print(f"✓ Created location with ID: {data['id']}")
    return data["id"]

def test_get_all_locations():
    print("\n--- Testing Get All Locations ---")
    response = requests.get(f"{API_URL}/api/v1/locations", headers=HEADERS)
    assert response.status_code == 200, f"Get all failed: {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "Response should be a dict with 'data' and 'total' keys"
    assert "data" in data, "Response should have 'data' key"
    assert "total" in data, "Response should have 'total' key"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["total"] > 0
    # Verify observation_count field exists
    for location in data["data"]:
        assert "observation_count" in location, "Each location should have observation_count"
    print(f"✓ Retrieved {len(data['data'])} location(s) out of {data['total']} total")

def test_get_location(location_id):
    print("\n--- Testing Get Single Location ---")
    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 200, f"Get single failed: {response.status_code}"
    data = response.json()
    assert data["id"] == location_id
    assert "observation_count" in data, "Location should have observation_count"
    print(f"✓ Retrieved location ID: {location_id}")
    return data

def test_update_location(location_id):
    print("\n--- Testing Update Location ---")
    update_data = {
        "description": "Updated test location"
    }
    response = requests.put(f"{API_URL}/api/v1/locations/{location_id}", json=update_data, headers=HEADERS)
    assert response.status_code == 200, f"Update failed: {response.status_code}"
    data = response.json()
    assert data["description"] == update_data["description"]
    print(f"✓ Updated location ID: {location_id}")

def test_create_observation(location_id):
    print("\n--- Testing Create Observation ---")
    observation = {
        "species": "Rødstrupe",
        "date": datetime.now().isoformat(),
        "location_id": location_id,
        "notes": "Test observation",
        "category": "Fugl"
    }
    response = requests.post(f"{API_URL}/api/v1/observations", json=observation, headers=HEADERS)
    assert response.status_code == 201, f"Create failed: {response.status_code} - {response.text}"
    data = response.json()
    assert data["species"] == observation["species"]
    assert data["category"] == observation["category"]
    assert data["location_id"] == location_id
    assert "id" in data
    print(f"✓ Created observation with ID: {data['id']}")
    return data["id"]

def test_get_all_observations():
    print("\n--- Testing Get All Observations ---")
    response = requests.get(f"{API_URL}/api/v1/observations", headers=HEADERS)
    assert response.status_code == 200, f"Get all failed: {response.status_code}"
    data = response.json()
    assert isinstance(data, dict), "Response should be a dict with 'data' and 'total' keys"
    assert "data" in data, "Response should have 'data' key"
    assert "total" in data, "Response should have 'total' key"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert data["total"] > 0
    print(f"✓ Retrieved {len(data['data'])} observation(s) out of {data['total']} total")
    return data["data"]

def test_get_observation(observation_id):
    print("\n--- Testing Get Single Observation ---")
    response = requests.get(f"{API_URL}/api/v1/observations/{observation_id}", headers=HEADERS)
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
    response = requests.put(f"{API_URL}/api/v1/observations/{observation_id}", json=update_data, headers=HEADERS)
    assert response.status_code == 200, f"Update failed: {response.status_code}"
    data = response.json()
    assert data["notes"] == update_data["notes"]
    print(f"✓ Updated observation ID: {observation_id}")

def test_delete_observation(observation_id):
    print("\n--- Testing Delete Observation ---")
    response = requests.delete(f"{API_URL}/api/v1/observations/{observation_id}", headers=HEADERS)
    assert response.status_code == 204, f"Delete failed: {response.status_code}"

    # Verify deletion
    response = requests.get(f"{API_URL}/api/v1/observations/{observation_id}", headers=HEADERS)
    assert response.status_code == 404, "Observation should not exist after deletion"
    print(f"✓ Deleted observation ID: {observation_id}")

def test_delete_location(location_id):
    print("\n--- Testing Delete Location ---")
    response = requests.delete(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 204, f"Delete failed: {response.status_code}"

    # Verify deletion
    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 404, "Location should not exist after deletion"
    print(f"✓ Deleted location ID: {location_id}")

def test_observation_count_on_location():
    print("\n--- Testing Observation Count on Location ---")

    location = {
        "name": "Count Test Location",
        "latitude": 59.9139,
        "longitude": 10.7522
    }
    response = requests.post(f"{API_URL}/api/v1/locations", json=location, headers=HEADERS)
    assert response.status_code == 201
    location_id = response.json()["id"]

    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["observation_count"] == 0, "New location should have 0 observations"
    print("✓ New location has observation_count = 0")

    observation1 = {
        "species": "Test Bird 1",
        "date": datetime.now().isoformat(),
        "location_id": location_id,
        "category": "Fugl"
    }
    response = requests.post(f"{API_URL}/api/v1/observations", json=observation1, headers=HEADERS)
    assert response.status_code == 201
    obs1_id = response.json()["id"]

    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["observation_count"] == 1, "Location should have 1 observation"
    print("✓ After creating 1 observation, count = 1")

    observation2 = {
        "species": "Test Bird 2",
        "date": datetime.now().isoformat(),
        "location_id": location_id,
        "category": "Fugl"
    }
    response = requests.post(f"{API_URL}/api/v1/observations", json=observation2, headers=HEADERS)
    assert response.status_code == 201
    obs2_id = response.json()["id"]

    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["observation_count"] == 2, "Location should have 2 observations"
    print("✓ After creating 2 observations, count = 2")

    requests.delete(f"{API_URL}/api/v1/observations/{obs1_id}", headers=HEADERS)

    response = requests.get(f"{API_URL}/api/v1/locations/{location_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["observation_count"] == 1, "Location should have 1 observation after deleting one"
    print("✓ After deleting 1 observation, count = 1")

    requests.delete(f"{API_URL}/api/v1/observations/{obs2_id}", headers=HEADERS)
    requests.delete(f"{API_URL}/api/v1/locations/{location_id}")

def test_location_deletion_nullifies_observation():
    print("\n--- Testing Location Deletion Nullifies Observation Location ---")

    location = {
        "name": "Deletion Test Location",
        "latitude": 60.0,
        "longitude": 11.0
    }
    response = requests.post(f"{API_URL}/api/v1/locations", json=location)
    assert response.status_code == 201
    location_id = response.json()["id"]

    observation = {
        "species": "Deletion Test Bird",
        "date": datetime.now().isoformat(),
        "location_id": location_id,
        "category": "Fugl"
    }
    response = requests.post(f"{API_URL}/api/v1/observations", json=observation, headers=HEADERS)
    assert response.status_code == 201
    obs_id = response.json()["id"]

    response = requests.get(f"{API_URL}/api/v1/observations/{obs_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["location_id"] == location_id, "Observation should have location_id"
    assert response.json()["location"] is not None, "Observation should have location object"
    print("✓ Observation has location before deletion")

    requests.delete(f"{API_URL}/api/v1/locations/{location_id}")

    response = requests.get(f"{API_URL}/api/v1/observations/{obs_id}", headers=HEADERS)
    assert response.status_code == 200
    assert response.json()["location_id"] is None, "Observation location_id should be None after location deletion"
    assert response.json()["location"] is None, "Observation location should be None after location deletion"
    print("✓ Observation location_id and location are None after location deletion")

    requests.delete(f"{API_URL}/api/v1/observations/{obs_id}", headers=HEADERS)

def test_observation_sorting():
    print("\n--- Testing Observation Sorting ---")

    observations = [
        {"species": "Ørn", "date": "2024-01-01", "category": "Fugl", "notes": "Note A"},
        {"species": "Bjørn", "date": "2024-03-01", "category": "Pattedyr", "notes": "Note B"},
        {"species": "Rødstrupe", "date": "2024-02-01", "category": "Fugl", "notes": "Note C"},
    ]

    created_ids = []
    for obs in observations:
        response = requests.post(f"{API_URL}/api/v1/observations", json=obs, headers=HEADERS)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])

    response = requests.get(f"{API_URL}/api/v1/observations", params={"sort_by": "species", "sort_order": "asc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    species_list = [obs["species"] for obs in data]
    assert species_list == sorted(species_list), "Species should be sorted ascending"
    print("✓ Observations sorted by species (asc)")

    response = requests.get(f"{API_URL}/api/v1/observations", params={"sort_by": "species", "sort_order": "desc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    species_list = [obs["species"] for obs in data]
    assert species_list == sorted(species_list, reverse=True), "Species should be sorted descending"
    print("✓ Observations sorted by species (desc)")

    response = requests.get(f"{API_URL}/api/v1/observations", params={"sort_by": "date", "sort_order": "asc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    date_list = [obs["date"] for obs in data]
    assert date_list == sorted(date_list), "Dates should be sorted ascending"
    print("✓ Observations sorted by date (asc)")

    response = requests.get(f"{API_URL}/api/v1/observations", params={"sort_by": "category", "sort_order": "asc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    category_list = [obs["category"] for obs in data]
    assert category_list == sorted(category_list), "Categories should be sorted ascending"
    print("✓ Observations sorted by category (asc)")

    for obs_id in created_ids:
        requests.delete(f"{API_URL}/api/v1/observations/{obs_id}", headers=HEADERS)

def test_location_sorting():
    print("\n--- Testing Location Sorting ---")

    locations = [
        {"name": "Zoo", "address": "Address C", "latitude": 60.0, "longitude": 10.0},
        {"name": "Akvariet", "address": "Address A", "latitude": 59.0, "longitude": 11.0},
        {"name": "Museum", "address": "Address B", "latitude": 61.0, "longitude": 9.0},
    ]

    created_ids = []
    for loc in locations:
        response = requests.post(f"{API_URL}/api/v1/locations", json=loc, headers=HEADERS)
        assert response.status_code == 201
        created_ids.append(response.json()["id"])

    response = requests.get(f"{API_URL}/api/v1/locations", params={"sort_by": "name", "sort_order": "asc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    name_list = [loc["name"] for loc in data]
    assert name_list == sorted(name_list), "Names should be sorted ascending"
    print("✓ Locations sorted by name (asc)")

    response = requests.get(f"{API_URL}/api/v1/locations", params={"sort_by": "name", "sort_order": "desc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    name_list = [loc["name"] for loc in data]
    assert name_list == sorted(name_list, reverse=True), "Names should be sorted descending"
    print("✓ Locations sorted by name (desc)")

    response = requests.get(f"{API_URL}/api/v1/locations", params={"sort_by": "address", "sort_order": "asc"}, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()["data"]
    address_list = [loc["address"] if loc["address"] else "" for loc in data]
    assert address_list == sorted(address_list), "Addresses should be sorted ascending"
    print("✓ Locations sorted by address (asc)")

    for loc_id in created_ids:
        requests.delete(f"{API_URL}/api/v1/locations/{loc_id}", headers=HEADERS)

def run_tests():
    print("=" * 50)
    print("Starting API Tests (via Nginx)")
    print("=" * 50)

    if not wait_for_api():
        sys.exit(1)

    try:
        test_nginx_proxy()
        test_health_check()

        # Test locations
        location_id = test_create_location()
        test_get_all_locations()
        test_get_location(location_id)
        test_update_location(location_id)

        # Test observations with location
        observation_id = test_create_observation(location_id)
        test_get_all_observations()
        test_get_observation(observation_id)
        test_update_observation(observation_id)
        test_delete_observation(observation_id)

        # Delete location after observations are deleted
        test_delete_location(location_id)

        # Test observation count on locations
        test_observation_count_on_location()

        # Test location deletion nullifies observation location
        test_location_deletion_nullifies_observation()

        # Test sorting functionality
        test_observation_sorting()
        test_location_sorting()

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
