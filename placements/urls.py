from django.urls import path
from .views import home, dashboards, create_profile, view_profile, edit_profile, placement_dashboard,student_list, student_detail, job_list, apply_job, my_applications, update_status, application_list, create_job, announcements, post_announcement

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboards, name='dashboard'),
    path(
'profile/create/',
create_profile,
name='create_profile'
),
path(
'profile/',
view_profile,
name='view_profile'
),
path(
'profile/edit/',
edit_profile,
name='edit_profile'
),
path(
'placement/dashboard/',
placement_dashboard,
name='placement_dashboard'
),
path(
'placement/students/',
student_list,
name='student_list'
),
path(
'placement/student/<int:id>/',
student_detail,
name='student_detail'
),
path(
'jobs/',
job_list,
name='job_list'
),
path('jobs/', job_list, name='job_list'),
path('jobs/apply/<int:id>/', apply_job, name='apply_job'),
path('my-applications/', my_applications, name='my_applications'),
path('applications/update/<int:id>/', update_status, name='update_status'),
path('applications/', application_list, name='application_list'),
path('jobs/create/', create_job, name='create_job'),
path('announcements/', announcements, name='announcements'),
path('announcements/', announcements, name='announcements'),
path('announcements/post/', post_announcement, name='post_announcement'),
]
