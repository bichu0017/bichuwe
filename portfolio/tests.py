from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from .models import PortfolioDocument, Profile, Project, Resume


class PortfolioApiTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._media_directory = tempfile.TemporaryDirectory()
        cls._media_settings = override_settings(MEDIA_ROOT=cls._media_directory.name)
        cls._media_settings.enable()

    @classmethod
    def tearDownClass(cls):
        cls._media_settings.disable()
        cls._media_directory.cleanup()
        super().tearDownClass()

    def test_health_check_returns_ok_without_api_throttling(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_public_can_submit_contact_message(self):
        response = self.client.post(
            "/api/contact/",
            {"name": "Visitor", "email": "visitor@example.com", "message": "Hello"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)

    @override_settings(CORS_ALLOWED_ORIGINS=["https://portfolio.vercel.app"])
    def test_api_allows_configured_frontend_origin(self):
        response = self.client.get(
            "/api/profile/",
            HTTP_ORIGIN="https://portfolio.vercel.app",
        )
        self.assertEqual(
            response["access-control-allow-origin"],
            "https://portfolio.vercel.app",
        )

    def test_public_cannot_modify_skills(self):
        response = self.client.post("/api/skills/", {"name": "New skill", "category": "Testing"})
        self.assertEqual(response.status_code, 403)

    def test_only_admin_can_add_certificates_and_public_can_read_description(self):
        payload = {
            "title": "Machine Learning Fundamentals",
            "organization": "Example Academy",
            "description": "Completed an introductory course in machine learning.",
            "issue_date": "2026-10-01",
            "credential_url": "https://example.com/credential",
        }
        response = self.client.post("/api/certifications/", payload)
        self.assertEqual(response.status_code, 403)

        admin = get_user_model().objects.create_superuser(
            username="certificate-admin",
            email="certificate-admin@example.com",
            password="test-password",
        )
        self.client.force_authenticate(admin)
        response = self.client.post("/api/certifications/", payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["description"], payload["description"])

        self.client.force_authenticate(user=None)
        public_response = self.client.get("/api/certifications/")
        self.assertEqual(public_response.status_code, 200)
        self.assertEqual(public_response.data["results"][0]["description"], payload["description"])

    def test_admin_can_upload_pdf_and_word_certificate_files(self):
        admin = get_user_model().objects.create_superuser(
            username="certificate-file-admin",
            email="certificate-file-admin@example.com",
            password="test-password",
        )
        self.client.force_authenticate(admin)
        certificates = [
            ("PDF Certificate", "certificate.pdf", b"%PDF-1.4 example"),
            ("Word Certificate", "certificate.doc", b"Word certificate example"),
        ]
        for title, filename, content in certificates:
            response = self.client.post(
                "/api/certifications/",
                {
                    "title": title,
                    "organization": "Example Academy",
                    "certificate_file": SimpleUploadedFile(filename, content),
                },
                format="multipart",
            )
            self.assertEqual(response.status_code, 201, response.data)
            self.assertTrue(response.data["certificate_file"].endswith(filename))

    def test_admin_can_create_skill(self):
        admin = get_user_model().objects.create_superuser(
            username="portfolio-admin",
            email="admin@example.com",
            password="secure-test-password",
        )
        self.client.force_authenticate(admin)
        response = self.client.post("/api/skills/", {"name": "New skill", "category": "Testing"})
        self.assertEqual(response.status_code, 201)

    def test_public_only_sees_published_projects(self):
        Project.objects.create(title="Published project", description="Visible", category="Test", is_published=True)
        Project.objects.create(title="Draft project", description="Private", category="Test", is_published=False)
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Published project")

    def test_only_admin_can_upload_documents(self):
        response = self.client.post(
            "/api/documents/",
            {
                "title": "Project notes",
                "file": SimpleUploadedFile("notes.txt", b"Portfolio notes"),
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 403)

    def test_admin_can_upload_document_for_public_download(self):
        admin = get_user_model().objects.create_superuser(
            username="file-admin",
            email="files@example.com",
            password="secure-test-password",
        )
        self.client.force_authenticate(admin)
        response = self.client.post(
            "/api/documents/",
            {
                "title": "Project notes",
                "file": SimpleUploadedFile("notes.txt", b"Portfolio notes"),
                "is_published": True,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.client.force_authenticate(user=None)
        download = self.client.get(response.data["download_url"])
        self.assertEqual(download.status_code, 200)
        self.assertEqual(b"".join(download.streaming_content), b"Portfolio notes")
        download.close()

    def test_resume_download_only_serves_active_resume(self):
        Resume.objects.create(
            file=SimpleUploadedFile("resume.pdf", b"%PDF-1.4 example"),
            is_active=True,
        )
        response = self.client.get("/downloads/resume/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="resume.pdf"')
        response.close()

    def test_admin_dashboard_requires_staff_login(self):
        response = self.client.get("/admin-dashboard/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin-dashboard/login/", response["Location"])
        login_page = self.client.get("/admin-dashboard/login/")
        self.assertEqual(login_page.status_code, 200)

    def test_staff_profile_editor_shows_contact_and_social_fields(self):
        admin = get_user_model().objects.create_superuser(
            username="profile-editor",
            email="editor@example.com",
            password="secure-test-password",
        )
        self.client.force_login(admin)
        response = self.client.get("/admin-dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Full name")
        self.assertContains(response, "Email")
        self.assertContains(response, "Phone")
        self.assertContains(response, "Biography")
        self.assertContains(response, "Linkedin url")
        self.assertContains(response, "Manage certificates")

    def test_admin_dashboard_updates_profile_contact_and_social_details(self):
        admin = get_user_model().objects.create_superuser(
            username="profile-admin",
            email="profile-admin@example.com",
            password="secure-test-password",
        )
        self.client.force_login(admin)
        response = self.client.post(
            "/admin-dashboard/",
            {
                "full_name": "Bichu Biju Updated",
                "professional_title": "AI/ML Engineer",
                "introduction": "Building useful software.",
                "biography": "I enjoy working with AI.",
                "email": "bichu@example.com",
                "phone": "+911234567890",
                "location": "Kerala, India",
                "linkedin_url": "https://www.linkedin.com/in/bichu",
                "github_url": "https://github.com/bichu",
                "instagram_url": "https://www.instagram.com/bichu",
            },
        )
        self.assertRedirects(response, "/admin-dashboard/")
        profile = Profile.objects.get(full_name="Bichu Biju Updated")
        self.assertEqual(profile.email, "bichu@example.com")
        self.assertEqual(profile.phone, "+911234567890")
        self.assertEqual(profile.location, "Kerala, India")

    def test_admin_can_upload_three_profile_photos_and_api_exposes_them(self):
        admin = get_user_model().objects.create_superuser(
            username="profile-photo-admin",
            email="photo-admin@example.com",
            password="test-password",
        )
        self.client.force_login(admin)
        image_buffer = BytesIO()
        Image.new("RGB", (1, 1)).save(image_buffer, format="PNG")
        photo_data = image_buffer.getvalue()
        response = self.client.post(
            "/admin-dashboard/",
            {
                "full_name": "Photo Admin",
                "professional_title": "AI/ML Engineer",
                "profile_image": SimpleUploadedFile("photo-1.png", photo_data, content_type="image/png"),
                "profile_image_2": SimpleUploadedFile("photo-2.png", photo_data, content_type="image/png"),
                "profile_image_3": SimpleUploadedFile("photo-3.png", photo_data, content_type="image/png"),
            },
        )
        self.assertRedirects(response, "/admin-dashboard/")

        profile = Profile.objects.get(full_name="Photo Admin")
        self.assertEqual(profile.profile_image.name.rsplit("/", 1)[-1], "photo-1.png")
        self.assertEqual(profile.profile_image_2.name.rsplit("/", 1)[-1], "photo-2.png")
        self.assertEqual(profile.profile_image_3.name.rsplit("/", 1)[-1], "photo-3.png")

        api_response = self.client.get("/api/profile/")
        self.assertEqual(api_response.status_code, 200)
        api_profile = api_response.data["results"][0]
        self.assertEqual(api_profile["profile_image"], f"http://testserver{profile.profile_image.url}")
        self.assertEqual(api_profile["profile_image_2"], f"http://testserver{profile.profile_image_2.url}")
        self.assertEqual(api_profile["profile_image_3"], f"http://testserver{profile.profile_image_3.url}")

    def test_public_page_renders_contact_csrf_token(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
