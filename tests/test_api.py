# from fastapi.testclient import TestClient

# from api.main import BOUNDING_BOX_ROUTER_PREFIX, app

# client = TestClient(app)


# def test_guest_permissions():
#     response1 = client.get(BOUNDING_BOX_ROUTER_PREFIX)
#     response2 = client.get(f"{BOUNDING_BOX_ROUTER_PREFIX}/2")
#     for response in [response1, response2]:
#         assert response.status_code == 403
