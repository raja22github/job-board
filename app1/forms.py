from django import forms
from .models import Job, JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'salary', 'job_type', 'category', 'company']

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume']
        widgets = {
            'resume': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'application/pdf'
            }),
        }
    def clean_resume(self):
        resume = self.cleaned_data['resume']
        if not resume.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return resume