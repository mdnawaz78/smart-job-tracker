from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):

    class Meta:

        model = JobApplication

        fields = [
            "company_name",
            "job_title",
            "location",
            "application_date",
            "deadline",
            "status",
            "job_url",
            "salary",
            "notes",
        ]

        widgets = {

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter company name",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter job title",
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Bangalore / Remote",
                }
            ),

            "application_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "deadline": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "job_url": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://example.com/job",
                }
            ),

            "salary": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. 5 LPA",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add notes about this application...",
                    "rows": 5,
                }
            ),
        }