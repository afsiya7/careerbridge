from django import forms
from .models import StudentProfile, JobPosting
from .models import Announcement


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")
        return phone

    def clean_passout_year(self):
        year = self.cleaned_data.get('passout_year')
        if year < 2000 or year > 2030:
            raise forms.ValidationError("Enter a valid passout year between 2000 and 2030.")
        return year

    def clean_github(self):
        github = self.cleaned_data.get('github')
        if github and 'github.com' not in github:
            raise forms.ValidationError("Enter a valid GitHub URL.")
        return github

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get('linkedin')
        if linkedin and 'linkedin.com' not in linkedin:
            raise forms.ValidationError("Enter a valid LinkedIn URL.")
        return linkedin

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError("Resume must be a PDF file.")
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Resume file size must be under 5MB.")
        return resume

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        if not skills or len(skills.strip()) < 3:
            raise forms.ValidationError("Please enter at least one skill.")
        return skills


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'company_name',
            'job_title',
            'location',
            'package',
            'apply_link',
            'description',
            'company_logo',
            'image',
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'package': forms.TextInput(attrs={'class': 'form-control'}),
            'apply_link': forms.URLInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_company_logo(self):
        logo = self.cleaned_data.get('company_logo')
        if logo:
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = '.' + logo.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise forms.ValidationError("Only JPG, PNG, and GIF images are allowed.")
            if logo.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Image size must be under 2MB.")
        return logo

    def clean_apply_link(self):
        link = self.cleaned_data.get('apply_link')
        if link and not (link.startswith('http://') or link.startswith('https://')):
            raise forms.ValidationError("Enter a valid URL starting with http:// or https://")
        return link


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'description', 'event_date', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }