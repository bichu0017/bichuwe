from django.http import FileResponse
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.utils.text import get_valid_filename
from django.views import View
from rest_framework import mixins, permissions, viewsets

from .models import (
    Achievement,
    Certification,
    ContactMessage,
    Education,
    Profile,
    PortfolioDocument,
    Project,
    Resume,
    Skill,
    VisitorQuestion,
    WebsiteSettings,
)
from .forms import ProfileEditorForm
from .serializers import (
    AchievementSerializer,
    CertificationSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ProfileSerializer,
    PortfolioDocumentSerializer,
    ProjectSerializer,
    ResumeSerializer,
    SkillSerializer,
    VisitorQuestionSerializer,
    WebsiteSettingsSerializer,
)


@staff_member_required(login_url="/admin-dashboard/login/")
def profile_editor(request):
    profile = Profile.objects.order_by("pk").first()
    if profile is None:
        profile = Profile()

    if request.method == "POST":
        form = ProfileEditorForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile details saved.")
            return redirect("profile-editor")
    else:
        form = ProfileEditorForm(instance=profile)

    return render(request, "admin/profile_editor.html", {"form": form})


class PublicModelViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        permission_class = permissions.IsAdminUser if self.request.method not in permissions.SAFE_METHODS else permissions.AllowAny
        return [permission_class()]


class ProfileViewSet(PublicModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class SkillViewSet(PublicModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectViewSet(PublicModelViewSet):
    serializer_class = ProjectSerializer
    lookup_field = "slug"

    def get_queryset(self):
        queryset = Project.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset


class EducationViewSet(PublicModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class CertificationViewSet(PublicModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer


class AchievementViewSet(PublicModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class ResumeViewSet(PublicModelViewSet):
    queryset = Resume.objects.filter(is_active=True).order_by("-uploaded_at")
    serializer_class = ResumeSerializer


class PortfolioDocumentViewSet(PublicModelViewSet):
    serializer_class = PortfolioDocumentSerializer

    def get_queryset(self):
        queryset = PortfolioDocument.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset


class ResumeDownloadView(View):
    def get(self, request):
        from .models import Resume

        resume = get_object_or_404(Resume.objects.filter(is_active=True).order_by("-uploaded_at"))
        return FileResponse(
            resume.file.open("rb"),
            as_attachment=True,
            filename=get_valid_filename(resume.file.name.rsplit("/", 1)[-1]),
            content_type="application/octet-stream",
        )


class DocumentDownloadView(View):
    def get(self, request, document_id):
        document = get_object_or_404(PortfolioDocument, pk=document_id, is_published=True)
        return FileResponse(
            document.file.open("rb"),
            as_attachment=True,
            filename=get_valid_filename(document.file.name.rsplit("/", 1)[-1]),
            content_type="application/octet-stream",
        )


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [permissions.AllowAny]


class QuestionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = VisitorQuestionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return VisitorQuestion.objects.filter(is_published=True)


class WebsiteSettingsViewSet(PublicModelViewSet):
    queryset = WebsiteSettings.objects.all()
    serializer_class = WebsiteSettingsSerializer
