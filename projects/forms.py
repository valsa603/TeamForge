from django import forms
from .models import Project,Task


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = [
            "title",
            "description",
            "required_skills",
            "team_size",
            "deadline",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter project name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe your project",
                    "rows": 5
                }
            ),

            "required_skills": forms.CheckboxSelectMultiple(),

            "team_size": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 20
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }

        from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "assigned_to",
            "status",
            "deadline",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter task title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the task",
                    "rows": 4
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),
        }