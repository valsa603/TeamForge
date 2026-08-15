from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "college",
            "branch",
            "year",
            "bio",
            "skills",
        ]

        widgets = {
            "college": forms.TextInput(
                attrs={"placeholder": "Enter your college"}
            ),

            "branch": forms.TextInput(
                attrs={"placeholder": "Example: ECE"}
            ),

            "year": forms.TextInput(
                attrs={"placeholder": "Example: 2nd Year"}
            ),

            "bio": forms.Textarea(
                attrs={
                    "placeholder": "Tell us about yourself",
                    "rows": 4
                }
            ),

            "skills": forms.CheckboxSelectMultiple(),
        }