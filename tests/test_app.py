import unittest
from unittest.mock import patch

from app import app


class StarterSiteTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_home_page_renders(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("File Forge 1.0", response.get_data(as_text=True))
        self.assertIn("A Windows desktop utility", response.get_data(as_text=True))

    def test_public_utility_routes_render(self):
        for path in ("/robots.txt", "/sitemap.xml", "/health"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_future_studio_pages_are_not_routed(self):
        for path in ("/worlds", "/about", "/contact"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)

    def test_tools_page_has_file_forge_release_download_and_repo_links(self):
        response = self.client.get("/tools")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        body = self.client.get("/").get_data(as_text=True)
        self.assertIn("File Forge 1.0", body)
        self.assertIn("Download for Windows", body)
        self.assertIn("View on GitHub", body)
        self.assertIn("fileforge-1.0-windows-x64.zip", body)
        self.assertIn("Windows SmartScreen may show an unknown-publisher warning", body)
        self.assertIn("View the VirusTotal report for this exact build", body)
        self.assertIn("c5a51af9905fb5c8827691f8b2417c3233f10c4d53ee5085d86005b3d7dcc98f", body)
        self.assertIn("https://github.com/andrewmock96/FileForge", body)
        self.assertIn("buying the developer a Mountain Dew", body)
        self.assertIn("https://ko-fi.com/mockinteractive", body)
        self.assertIn("Buy Ginger Dev a Mountain Dew", body)
        self.assertIn("Only required for the initial download and optional support links", body)
        self.assertIn("Saved you some time or a headache?", body)
        self.assertIn("remember separate starting folders", body)
        self.assertIn("Refreshes available destination capacity every five seconds", body)
        self.assertIn("Optional full input and finished-output verification can be disabled", body)
        self.assertIn("cannot fully verify every source or output byte", body)
        self.assertIn("ISO", body)
        self.assertIn("GOD", body)
        self.assertIn("XEX", body)

        screenshot = self.client.get("/static/images/tools/file-forge-ui.png")
        self.assertEqual(screenshot.status_code, 200)
        self.assertGreater(len(screenshot.data), 1_000_000)

    def test_brand_icons_are_linked_and_served(self):
        body = self.client.get("/").get_data(as_text=True)
        for path in (
            "/static/favicon.ico",
            "/static/images/brand/favicon-48.png",
            "/static/images/brand/favicon-192.png",
            "/static/images/brand/apple-touch-icon.png",
            "/static/site.webmanifest",
        ):
            with self.subTest(path=path):
                self.assertIn(path, body)
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertGreater(len(response.data), 100)
                response.close()

    def test_cloudflare_analytics_is_enabled_only_with_a_token(self):
        with patch.dict(
            "os.environ", {"CLOUDFLARE_WEB_ANALYTICS_TOKEN": "test-token"}
        ):
            body = self.client.get("/").get_data(as_text=True)
        self.assertIn("https://static.cloudflareinsights.com/beacon.min.js", body)
        self.assertIn('data-cf-beacon=\'{"token":"test-token"}\'', body)

    def test_mobile_hero_focuses_the_disc(self):
        response = self.client.get("/static/css/style.css")
        self.assertEqual(response.status_code, 200)
        css = response.get_data(as_text=True)
        self.assertIn("background-position: 35% center", css)
        response.close()

    def test_health_check_reports_ok(self):
        self.assertEqual(self.client.get("/health").get_json(), {"status": "ok"})

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
