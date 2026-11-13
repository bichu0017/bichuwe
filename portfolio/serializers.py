from rest_framework import serializers

from .models import (
    Achievement,
    Certification,
    ContactMessage,
    Education,
    Profile,
    PortfolioDocument,
    Project,
    ProjectImage,
    Resume,
    Skill,
    VisitorQuestion,
    WebsiteSettings,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = "__all__"


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = "__all__"


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = "__all__"


class ResumeSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = Resume
        fields = ["id", "file", "description", "uploaded_at", "is_active", "download_url"]
        read_only_fields = ["id", "uploaded_at", "download_url"]

    def get_download_url(self, obj):
        from django.urls import reverse

        return reverse("resume-download")


class PortfolioDocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    file_name = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = PortfolioDocument
        fields = ["id", "title", "description", "file", "file_name", "uploaded_at", "is_published", "download_url"]
        read_only_fields = ["id", "uploaded_at", "file_name", "download_url"]

    def get_file_name(self, obj):
        return obj.file.name.rsplit("/", 1)[-1]

    def get_download_url(self, obj):
        from django.urls import reverse

        return reverse("document-download", args=[obj.pk])


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "is_read", "created_at"]
        read_only_fields = ["id", "is_read", "created_at"]


class VisitorQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorQuestion
        fields = "__all__"
        read_only_fields = ["id", "answer", "is_published", "created_at"]


class WebsiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteSettings
        fields = "__all__"
