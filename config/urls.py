from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from portfolio.views import (
    AchievementViewSet,
    CertificationViewSet,
    ContactMessageViewSet,
    EducationViewSet,
    DocumentDownloadView,
    ProfileViewSet,
    PortfolioDocumentViewSet,
    ProjectViewSet,
    QuestionViewSet,
    ResumeViewSet,
    SkillViewSet,
    WebsiteSettingsViewSet,
    ResumeDownloadView,
    profile_editor,
)

router = DefaultRouter()
router.register("profile", ProfileViewSet, basename="profile")
router.register("skills", SkillViewSet, basename="skill")
router.register("projects", ProjectViewSet, basename="project")
router.register("education", EducationViewSet, basename="education")
router.register("certifications", CertificationViewSet, basename="certification")
router.register("achievements", AchievementViewSet, basename="achievement")
router.register("resume", ResumeViewSet, basename="resume")
router.register("documents", PortfolioDocumentViewSet, basename="document")
router.register("contact", ContactMessageViewSet, basename="contact")
router.register("questions", QuestionViewSet, basename="question")
router.register("settings", WebsiteSettingsViewSet, basename="settings")


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("health/", health_check, name="health-check"),
    path("admin-dashboard/", profile_editor, name="profile-editor"),
    path("admin-dashboard/", admin.site.urls),
    path("downloads/resume/", ResumeDownloadView.as_view(), name="resume-download"),
    path("downloads/documents/<int:document_id>/", DocumentDownloadView.as_view(), name="document-download"),
    path("api/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
