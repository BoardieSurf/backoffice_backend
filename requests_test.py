import requests

session = requests.session()

r1 = session.post(
    "http://localhost:8000/superuser/create_rental_business_register_invite",
    json={"email": "user@example.com"},
)

assert r1.status_code == 200

invite_token = input("insert token:")

register_body = {
    "phone": "fake phone",
    "address": "fake address",
    "business_title": "best surf school",
    "business_description": "the best surf school ever!!!",
    "business_type": "school",
    "username": "alex",
    "password": "password",
    "register_token": invite_token,
}

r2 = session.post("http://localhost:8000/backoffice/register", json=register_body)

assert r2.status_code == 200

r3 = session.post(
    "http://localhost:8000/backoffice/login",
    json={"username": "alex", "password": "password"},
)

assert r3.status_code == 200
session.headers = {"access_token": r3.json()["data"]["token"]}

r4 = session.get("http://localhost:8000/backoffice/info")
assert r4.status_code == 200
assert r4.json()["data"]["phone"] == "fake phone"

register_body["phone"] = "new fake phone"
r5 = session.put("http://localhost:8000/backoffice/info", json=register_body)
assert r5.status_code == 200

r6 = session.get("http://localhost:8000/backoffice/info")
assert r6.status_code == 200
assert r6.json()["data"]["phone"] == "new fake phone"

r7 = session.get("http://localhost:8000/backoffice/info/image")
assert r7.status_code == 200
assert r7.json()["data"] == []

files = {"file": open("test_image.jpeg", "rb")}
r8 = session.post("http://localhost:8000/backoffice/info/image", files=files)
assert r8.status_code == 200

r9 = session.get("http://localhost:8000/backoffice/info/image")
assert r9.status_code == 200
assert len(r9.json()["data"]) == 1
assert r9.json()["data"][0]["is_main"]
main_pic_id = r9.json()["data"][0]["private_id"]


files = {"file": open("test_image.jpeg", "rb")}
r10 = session.post("http://localhost:8000/backoffice/info/image", files=files)
assert r10.status_code == 200

r11 = session.get("http://localhost:8000/backoffice/info/image")
assert r11.status_code == 200
assert len(r11.json()["data"]) == 2
assert r11.json()["data"][1]["is_main"] is False
not_main_pic_id = r11.json()["data"][1]["private_id"]


r12 = session.get(
    f"http://localhost:8000/backoffice/info/image/{not_main_pic_id}/set_as_main"
)
assert r12.status_code == 200

r13 = session.get("http://localhost:8000/backoffice/info/image")
assert r13.status_code == 200
assert len(r13.json()["data"]) == 2
assert r13.json()["data"][1]["is_main"] is True
