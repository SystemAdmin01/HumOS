import http.client
import json
import threading
import unittest

from linghos.web import HumOSHTTPRequestHandler, ReusableHTTPServer


class CockpitHTTPSecurityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ReusableHTTPServer(("127.0.0.1", 0), HumOSHTTPRequestHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection("127.0.0.1", self.port, timeout=3)
        connection.request(method, path, body=body, headers=headers or {})
        response = connection.getresponse()
        payload = response.read()
        result = (response.status, response.getheaders(), payload)
        connection.close()
        return result

    def test_rejects_cross_origin_post(self):
        status, _, payload = self.request(
            "POST",
            "/api/compile",
            body=json.dumps({"code": "Main() {}"}),
            headers={
                "Content-Type": "application/json",
                "Origin": "https://attacker.example",
            },
        )
        self.assertEqual(status, 403)
        self.assertIn(b"Cross-origin", payload)

    def test_requires_json_content_type(self):
        status, _, _ = self.request(
            "POST",
            "/api/compile",
            body='{"code":"Main() {}"}',
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(status, 415)

    def test_rejects_oversized_request_body(self):
        body = " " * (1024 * 1024 + 1)
        status, _, payload = self.request(
            "POST",
            "/api/compile",
            body=body,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 413)
        self.assertIn(b"1 MiB", payload)

    def test_rejects_malformed_json(self):
        status, _, payload = self.request(
            "POST",
            "/api/compile",
            body="{not-json",
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(status, 400)
        self.assertIn(b"valid UTF-8 JSON", payload)

    def test_accepts_same_origin_json_request(self):
        status, headers, payload = self.request(
            "POST",
            "/api/compile",
            body=json.dumps({"code": "Main() { Call >> Ice_shield; }"}),
            headers={
                "Content-Type": "application/json",
                "Origin": f"http://127.0.0.1:{self.port}",
                "Sec-Fetch-Site": "same-origin",
            },
        )
        self.assertEqual(status, 200)
        self.assertTrue(any(k.lower() == "cache-control" and v == "no-store" for k, v in headers))
        result = json.loads(payload.decode("utf-8"))
        self.assertIn("compiler_meta", result)
        self.assertIn("telemetry", result)

    def test_options_does_not_enable_cross_origin_access(self):
        status, headers, _ = self.request(
            "OPTIONS",
            "/api/compile",
            headers={"Origin": "https://attacker.example"},
        )
        self.assertEqual(status, 204)
        self.assertFalse(any(k.lower() == "access-control-allow-origin" for k, _ in headers))


if __name__ == "__main__":
    unittest.main()
