import unittest

from app import app


class StarterSiteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("We forge worlds", response.get_data(as_text=True))
        self.assertIn("Independent game studio", response.get_data(as_text=True))

    def test_public_pages_render(self):
        for path in ("/about", "/contact", "/robots.txt", "/sitemap.xml", "/health"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_health_check_reports_ok(self):
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok"})

    def test_contact_page_accepts_messages(self):
        response = self.client.post(
            "/contact",
            data={"name": "Ada", "email": "ada@example.com", "message": "Hello"},
            follow_redirects=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/contact")

    def test_contact_page_rejects_invalid_email_and_keeps_form_data(self):
        response = self.client.post(
            "/contact",
            data={"name": "Ada", "email": "invalid", "message": "Hello"},
        )
        body = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please enter a valid email address.", body)
        self.assertIn('value="Ada"', body)

    def test_unknown_page_uses_404_template(self):
        response = self.client.get("/missing")
        self.assertEqual(response.status_code, 404)
        self.assertIn("The trail ends here.", response.get_data(as_text=True))

    def test_security_headers_are_set(self):
        response = self.client.get("/")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")


if __name__ == "__main__":
    unittest.main()
