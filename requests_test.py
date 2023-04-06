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

r14 = session.get("http://localhost:8000/backoffice/board/")
assert r14.status_code == 200
assert len(r14.json()["data"]) == 0

r15 = session.post(
    "http://localhost:8000/backoffice/board/",
    json={
        "title": "Board 1",
        "description": "description of board 1",
        "category": "longboard",
        "replicas": 1,
    },
)
assert r15.status_code == 200

r16 = session.get("http://localhost:8000/backoffice/board/")
assert r16.status_code == 200
assert len(r16.json()["data"]) == 1

r17 = session.post(
    "http://localhost:8000/backoffice/board/",
    json={
        "title": "Foam Board 1",
        "description": "description of foam board 1",
        "category": "foamboard",
        "replicas": 2,
    },
)
assert r17.status_code == 200

r18 = session.get("http://localhost:8000/backoffice/board/")
assert r18.status_code == 200
assert len(r18.json()["data"]) == 3
board_id = r18.json()["data"][2]["private_id"]

r19 = session.delete(f"http://localhost:8000/backoffice/board/{board_id}")
assert r19.status_code == 200

r20 = session.get("http://localhost:8000/backoffice/board/")
assert r20.status_code == 200
assert len(r20.json()["data"]) == 2


r21 = session.get("http://localhost:8000/backoffice/board/")
assert r21.status_code == 200
assert len(r21.json()["data"]) == 2
board_id = r21.json()["data"][0]["private_id"]

r22 = session.put(
    f"http://localhost:8000/backoffice/board/{board_id}",
    json={
        "title": "MODIFIED NEW",
        "description": "MODIFIED NEW DESC",
        "category": "gun",
    },
)
assert r22.status_code == 200

r23 = session.get("http://localhost:8000/backoffice/board/")
assert r23.status_code == 200
board_obj = None
for board in r23.json()["data"]:
    if board["private_id"] == board_id:
        board_obj = board
        break
assert board_obj
assert board_obj["title"] == "MODIFIED NEW"


r24 = session.get("http://localhost:8000/backoffice/board/")
assert r24.status_code == 200
assert len(r24.json()["data"]) == 2
board_id = r24.json()["data"][0]["private_id"]

r25 = session.get(f"http://localhost:8000/backoffice/board/{board_id}/image")
assert r25.status_code == 200
assert len(r25.json()["data"]) == 0

files = {"file": open("test_image.jpeg", "rb")}
r26 = session.post(
    f"http://localhost:8000/backoffice/board/{board_id}/image", files=files
)
assert r26.status_code == 200

r27 = session.get(f"http://localhost:8000/backoffice/board/{board_id}/image")
assert r27.status_code == 200
assert len(r27.json()["data"]) == 1

r28 = session.get(f"http://localhost:8000/backoffice/board/{board_id}/image")
assert r28.status_code == 200
print(r28.json()["data"][0])
assert r28.json()["data"][0]["is_main"] is True

files = {"file": open("test_image.jpeg", "rb")}
r29 = session.post(
    f"http://localhost:8000/backoffice/board/{board_id}/image", files=files
)
assert r29.status_code == 200


r30 = session.get(f"http://localhost:8000/backoffice/board/{board_id}/image")
assert r30.status_code == 200
assert len(r30.json()["data"]) == 2
image_id = [x for x in r30.json()["data"] if x["is_main"] is False][0]["private_id"]

r31 = session.get(
    f"http://localhost:8000/backoffice/board/{board_id}/image/{image_id}/set_as_main"
)
assert r31.status_code == 200

r32 = session.get(f"http://localhost:8000/backoffice/board/{board_id}/image")
assert r32.status_code == 200
assert [x for x in r32.json()["data"] if x["is_main"] is True][0][
    "private_id"
] == image_id
