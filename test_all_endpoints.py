"""Test suite to verify all CBSE API endpoints."""

import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestCBSEBackend(unittest.TestCase):
    def test_test_db(self):
        response = client.get("/api/test-db")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))

    def test_list_circulars(self):
        response = client.get("/api/circulars")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("records_retrieved", data)
        self.assertIn("circulars", data)
        self.assertGreater(len(data["circulars"]), 0)

    def test_get_single_circular(self):
        # Get list first to pick a circular id
        list_res = client.get("/api/circulars")
        circular_id = list_res.json()["circulars"][0]["id"]
        response = client.get(f"/api/circulars/{circular_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], circular_id)

    def test_important_dates(self):
        response = client.get("/api/important-dates")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("important_dates", data)

    def test_news(self):
        response = client.get("/api/news")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("news", data)

    def test_search(self):
        response = client.get("/api/search?q=exam")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertGreater(data["records_retrieved"], 0)

    def test_services(self):
        response = client.get("/api/services?role=student")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("services", data)

    def test_user_profile(self):
        get_res = client.get("/api/user/profile")
        self.assertEqual(get_res.status_code, 200)

        put_res = client.put("/api/user/profile", json={"role": "student", "class": "10", "school": "DPS"})
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.json()["role"], "student")

    def test_notifications(self):
        res = client.get("/api/notifications")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("notifications", data)
        if data["notifications"]:
            nid = data["notifications"][0]["id"]
            read_res = client.put(f"/api/notifications/{nid}/read")
            self.assertEqual(read_res.status_code, 200)
            self.assertTrue(read_res.json()["read"])

    def test_ai_ask(self):
        res = client.post("/api/ai/ask", json={"message": "What are the rules for exam?"})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("answer", data)
        self.assertIn("sources", data)

    def test_ai_summarize(self):
        # Pick circular id from list
        list_res = client.get("/api/circulars")
        circular_id = list_res.json()["circulars"][0]["id"]
        res = client.post(f"/api/ai/summarize/{circular_id}")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("summary", data)
        self.assertIn("key_points", data)
        self.assertIn("important_dates", data)
        self.assertIn("required_actions", data)

if __name__ == "__main__":
    unittest.main()

