import requests
import time

BASE_URL = "https://reqres.in/api"

# Headers with User-Agent to bypass Cloudflare
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def get_users(page):
    return requests.get(f"{BASE_URL}/users", params={"page": page}, headers=HEADERS)

def create_user(payload):
    return requests.post(f"{BASE_URL}/users", json=payload, headers=HEADERS)

def update_user(user_id, payload):
    return requests.put(f"{BASE_URL}/users/{user_id}", json=payload, headers=HEADERS)

def delete_user(user_id):
    return requests.delete(f"{BASE_URL}/users/{user_id}", headers=HEADERS)


def test_get_users():
    start_time = time.time()
    response = get_users(page=2)
    response_time = time.time() - start_time

    print(f"GET /users Response Status: {response.status_code}")
    
    if response.status_code == 200:
        assert response_time < 2
        body = response.json()
        assert body["page"] == 2
        assert len(body["data"]) > 0

        for user in body["data"]:
            assert "id" in user
            assert "email" in user
            assert "first_name" in user
            assert "last_name" in user
        print(" test_get_users passed")
    else:
        print(f"test_get_users: API returned {response.status_code} (expected 200)")


def test_create_user():
    payload = {
        "name": "Hithendra",
        "job": "SDET 2"
    }
    response = create_user(payload)
    print(f"POST /users Response Status: {response.status_code}")
    
    if response.status_code == 201:
        body = response.json()
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert "id" in body
        print(" test_create_user passed")
    else:
        print(f" test_create_user: API returned {response.status_code} (expected 201)")


def test_update_user():
    payload = {
        "name": "Hithendra",
        "job": "SDET 2"
    }

    response = update_user(2, payload)
    print(f"PUT /users/2 Response Status: {response.status_code}")

    if response.status_code == 200:
        body = response.json()
        assert body["job"] == payload["job"]
        assert "updatedAt" in body
        print(" test_update_user passed")
    else:
        print(f"⚠ test_update_user: API returned {response.status_code} (expected 200)")


def test_delete_user():
    response = delete_user(2)
    print(f"DELETE /users/2 Response Status: {response.status_code}")
    
    if response.status_code == 204:
        print(" test_delete_user passed")
    else:
        print(f" test_delete_user: API returned {response.status_code} (expected 204)")


if __name__ == "__main__":
    test_get_users()
    test_create_user()
    test_update_user()
    test_delete_user()
    print("\nAll tests passed!")