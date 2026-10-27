
from fastapi.testclient import TestClient
from main import app, students

client = TestClient(app)

def setup_function():
    students.clear()

def test_home():
    assert client.get("/").status_code == 200

def test_add_student():
    r = client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 85
    })
    assert r.status_code == 201
    assert r.json()["name"] == "Sam"

def test_invalid_marks():
    r = client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 150
    })
    assert r.status_code == 422

def test_get_students():
    client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 85
    })
    assert len(client.get("/students").json()) == 1

def test_get_student():
    client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 85
    })
    assert client.get("/students/1").json()["name"] == "Sam"

def test_not_found():
    assert client.get("/students/999").status_code == 404

def test_duplicate():
    data = {"name": "Sam", "roll_no": "MCA029", "marks": 85}
    client.post("/students", json=data)
    assert client.post("/students", json=data).status_code == 409

def test_update():
    client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 85
    })
    r = client.put("/students/1", json={
        "name": "Sam Kumar", "roll_no": "MCA029", "marks": 90
    })
    assert r.status_code == 200
    assert r.json()["marks"] == 90

def test_delete():
    client.post("/students", json={
        "name": "Sam", "roll_no": "MCA029", "marks": 85
    })
    assert client.delete("/students/1").status_code == 200
    assert client.get("/students/1").status_code == 404
