from django.contrib import admin

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


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "is_published", "created_at")
    list_filter = ("category", "featured", "is_published")
    search_fields = ("title", "description", "technologies")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")


@admin.register(VisitorQuestion)
class VisitorQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "name", "is_published", "created_at")
    list_filter = ("is_published", "created_at")
    search_fields = ("question", "name", "email", "answer")


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Education)
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "issue_date")
    search_fields = ("title", "organization", "description")
    ordering = ("-issue_date", "title")
    fields = (
        "title",
        "organization",
        "description",
        "certificate_image",
        "certificate_file",
        "issue_date",
        "credential_url",
    )


admin.site.register(Achievement)
admin.site.register(Resume)
@admin.register(PortfolioDocument)
class PortfolioDocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "file", "uploaded_at", "is_published")
    list_filter = ("is_published", "uploaded_at")
    search_fields = ("title", "description", "file")


admin.site.register(WebsiteSettings)
