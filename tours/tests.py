from rest_framework.test import APITestCase


class TourOperatorTests(APITestCase):
    def setUp(self):
        self.tour = {"title": "Canyon", "destination": "Kazakhstan", "price": "149.00", "start_date": "2027-06-10", "end_date": "2027-06-12", "max_guests": 12}

    def test_complete_crud_and_relationship(self):
        response = self.client.post("/api/tours/", self.tour)
        self.assertEqual(response.status_code, 201)
        url = f"/api/tours/{response.data['id']}/"
        self.assertEqual(len(self.client.get("/api/tours/").data), 1)
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertEqual(self.client.put(url, self.tour).status_code, 200)
        self.assertEqual(self.client.patch(url, {"price": "199.00"}).data["price"], "199.00")
        booking = {"tour": response.data["id"], "customer_name": "Aida", "customer_email": "aida@example.com", "guests": 2}
        created = self.client.post("/api/bookings/", booking)
        self.assertEqual(created.status_code, 201)
        booking_url = f"/api/bookings/{created.data['id']}/"
        self.assertEqual(len(self.client.get("/api/bookings/").data), 1)
        self.assertEqual(self.client.get(booking_url).status_code, 200)
        self.assertEqual(self.client.put(booking_url, booking).status_code, 200)
        self.assertEqual(self.client.patch(booking_url, {"status": "confirmed"}).data["status"], "confirmed")
        self.assertEqual(self.client.delete(url).status_code, 409)
        self.assertEqual(self.client.delete(booking_url).status_code, 204)
        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_validation_and_partial_date_update(self):
        for field, value in [("price", "-1.00"), ("max_guests", 0), ("end_date", "2027-06-01"), ("title", "")]:
            self.assertEqual(self.client.post("/api/tours/", dict(self.tour, **{field: value})).status_code, 400)
        created = self.client.post("/api/tours/", self.tour)
        self.assertEqual(self.client.patch(f"/api/tours/{created.data['id']}/", {"start_date": "2027-07-01"}).status_code, 400)
        for overrides in [{"tour": 99999}, {"guests": 0}, {"customer_email": "invalid"}, {"status": "unknown"}]:
            booking = {"tour": created.data["id"], "customer_name": "Aida", "customer_email": "aida@example.com", "guests": 2}
            self.assertEqual(self.client.post("/api/bookings/", dict(booking, **overrides)).status_code, 400)

    def test_database_health(self):
        self.assertEqual(self.client.get("/api/health/").data, {"status": "ok", "database": "postgresql"})
