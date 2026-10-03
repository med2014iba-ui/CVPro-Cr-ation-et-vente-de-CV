import reflex as rx
import base64
import unittest
from unittest.mock import patch

from app.components.pdf_document import (
    _restricted_fetcher,
    build_cv_html,
    render_cv_pdf,
)


class PDFDocumentTests(unittest.TestCase):
    def test_escaping_and_five_a4_styles(self):
        information = {
            "first_name": "<script>alert(1)</script>",
            "last_name": "Test",
            "job_title": "Ingénieur",
            "summary": "Résumé & détails",
            "website": "https://example.invalid",
            "photo_filename": "",
        }
        sections = [
            {
                "label": "Expérience",
                "title": "<img src=x>",
                "organization": "Organisation",
                "period": "2020–2024",
                "details": "Travail\nRésultats",
            }
        ]
        for code in (
            "moderne",
            "classique",
            "elegant",
            "minimaliste",
            "creatif",
        ):
            with self.subTest(code=code):
                html = build_cv_html(information, sections, code)
                self.assertIn(f'class="{code}"', html)
                self.assertIn("size: A4", html)
                self.assertNotIn("<script>", html)
                self.assertIn("&lt;img src=x&gt;", html)
                self.assertIn("Organisation", html)
                self.assertTrue(
                    render_cv_pdf(information, sections, code).startswith(
                        b"%PDF-"
                    )
                )

    def test_fetcher_decodes_only_inline_base64_images(self):
        for mime in ("image/png", "image/jpeg", "image/webp"):
            with self.subTest(mime=mime):
                data = b"\x00\xff\x89image bytes"
                payload = base64.b64encode(data).decode("ascii")
                self.assertEqual(
                    _restricted_fetcher(f"data:{mime};base64,{payload}"),
                    {"string": data, "mime_type": mime},
                )

    def test_fetcher_rejects_external_and_invalid_uris(self):
        for url in (
            "https://example.invalid/photo.png",
            "http://example.invalid/photo.png",
            "file:///etc/passwd",
            "//example.invalid/photo.png",
            "/etc/passwd",
            "data:text/html;base64,SGVsbG8=",
            "data:image/;base64,SGVsbG8=",
            "data:image/png,SGVsbG8=",
            "data:image/png;charset=utf-8;base64,SGVsbG8=",
            "data:image/png;base64,",
            "data:image/png;base64,%%%",
            "data:image/png;base64,SGVsbG8",
            "data:image/png;base64,SGVsbG8===",
            "data:image/png;base64,SGVsbG8=\n",
            "data:image/png;base64,SGVsbG8=#fragment",
            "data:image/png;base64,SGVsbG8%3D",
            "data:image/png;base64,SGVsbG9=",
        ):
            with self.subTest(url=url):
                with self.assertRaises(ValueError):
                    _restricted_fetcher(url)

    def test_pdf_renders_inline_photo(self):
        uri = (
            "data:image/png;base64,"
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwC"
            "AAAAC0lEQVR42mP8/x8AAwMCAO+aC1sAAAAASUVORK5CYII="
        )
        with patch("app.components.pdf_document._photo_data", return_value=uri):
            pdf = render_cv_pdf(
                {"first_name": "Test", "last_name": "Photo"}, [], "moderne"
            )
        self.assertTrue(pdf.startswith(b"%PDF-"))

    def test_photo_path_is_not_client_controlled(self):
        with self.assertRaises(ValueError):
            build_cv_html({"photo_filename": "../../etc/passwd"}, [], "moderne")


if __name__ == "__main__":
    unittest.main()
