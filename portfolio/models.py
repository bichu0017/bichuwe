from django.core.files.storage import storages
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

from .validators import validate_certificate_file, validate_document_file, validate_image_size, validate_resume_file


class Profile(models.Model):
    full_name = models.CharField(max_length=120, default="Bichu Biju")
    professional_title = models.CharField(max_length=160, default="AI/ML Enthusiast")
    profile_image = models.ImageField(
        upload_to="profile/",
        storage=storages["profile_images"],
        blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
    )
    profile_image_2 = models.ImageField(
        upload_to="profile/",
        storage=storages["profile_images"],
        blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
    )
    profile_image_3 = models.ImageField(
        upload_to="profile/",
        storage=storages["profile_images"],
        blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            validate_image_size,
        ],
    )
    introduction = models.TextField(blank=True)
    biography = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=32, blank=True)
    location = models.CharField(max_length=120, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    def __str__(self):
        return self.full_name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="skills/", blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])
    proficiency = models.PositiveSmallIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(100)])
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=190, unique=True, blank=True)
    description = models.CharField(max_length=300)
    detailed_description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to="projects/", blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])
    technologies = models.JSONField(default=list, blank=True)
    github_url = models.URLField(blank=True)
    live_demo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-featured", "-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="projects/screenshots/", validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])
    caption = models.CharField(max_length=180, blank=True)

    def __str__(self):
        return f"{self.project.title} image"


class Education(models.Model):
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=180)
    department = models.CharField(max_length=180, blank=True)
    specialization = models.CharField(max_length=180, blank=True)
    start_year = models.PositiveSmallIntegerField()
    end_year = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_year"]

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=180)
    organization = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    certificate_image = models.ImageField(upload_to="certificates/", blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])
    certificate_file = models.FileField(
        upload_to="certificates/",
        blank=True,
        validators=[FileExtensionValidator(["pdf", "doc", "docx"]), validate_certificate_file],
    )
    issue_date = models.DateField(null=True, blank=True)
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return self.title


class Achievement(models.Model):
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    achievement_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to="achievements/", blank=True, validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])

    def __str__(self):
        return self.title


class Resume(models.Model):
    file = models.FileField(
        upload_to="resumes/",
        validators=[FileExtensionValidator(["pdf", "doc", "docx"]), validate_resume_file],
    )
    description = models.CharField(max_length=240, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Resume uploaded {self.uploaded_at:%Y-%m-%d}"


class PortfolioDocument(models.Model):
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to="documents/", validators=[validate_document_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField(max_length=5000)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject or self.message[:40]}"


class VisitorQuestion(models.Model):
    name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    question = models.TextField(max_length=2000)
    answer = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:80]


class WebsiteSettings(models.Model):
    website_title = models.CharField(max_length=180, default="Bichu Biju — AI/ML Enthusiast")
    favicon = models.ImageField(upload_to="site/", blank=True, validators=[FileExtensionValidator(["png", "ico"]), validate_image_size])
    footer_text = models.CharField(max_length=240, blank=True)
    contact_email = models.EmailField(blank=True)
    social_links = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.website_title
