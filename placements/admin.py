from django.contrib import admin
from .models import StudentProfile
from .models import Announcement
from .models import JobPosting
from .models import JobApplication
admin.site.register(
JobApplication
)
admin.site.register(
JobPosting
)
admin.site.register(
Announcement
)
admin.site.register(StudentProfile)