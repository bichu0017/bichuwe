from django import forms

from .models import Profile


class ProfileEditorForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "full_name",
            "professional_title",
            "profile_image",
            "profile_image_2",
            "profile_image_3",
            "introduction",
            "biography",
            "email",
            "phone",
            "location",
            "linkedin_url",
            "github_url",
            "instagram_url",
        ]
        widgets = {
            "introduction": forms.Textarea(attrs={"rows": 3}),
            "biography": forms.Textarea(attrs={"rows": 6}),
            "profile_image": forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
            "profile_image_2": forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
            "profile_image_3": forms.FileInput(attrs={"accept": "image/jpeg,image/png,image/webp"}),
        }
        labels = {
            "profile_image": "Photo 1",
            "profile_image_2": "Photo 2",
            "profile_image_3": "Photo 3",
        }
