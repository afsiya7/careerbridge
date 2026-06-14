from django.utils import timezone

from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import StudentProfileForm
from .models import StudentProfile
from accounts.decorators import placement_required
from collections import Counter
from .models import JobPosting
from .models import JobApplication
from .models import Announcement
from .forms import JobPostingForm, AnnouncementForm


def home(request):
    return render(request, 'home.html')


@login_required
def create_profile(request):
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('view_profile')
    else:
        form = StudentProfileForm()
    return render(request, 'profile/create_profile.html', {'form': form})


@login_required
def dashboards(request):
    today = timezone.now().date()
    announcements = Announcement.objects.filter(event_date__gte=today).order_by('event_date')
    student = StudentProfile.objects.get(user=request.user)
    my_applications = JobApplication.objects.filter(student=student)
    recent_jobs = JobPosting.objects.order_by('-created_at')[:5]
    profile_exists = StudentProfile.objects.filter(
        user=request.user
    ).exists()
    
    context = {
        'student': student,
        'announcements': announcements,
        'recent_jobs': recent_jobs,
        'my_applications': my_applications,
        'profile_exists': profile_exists,
        'announcements':announcements,
    }
    
    return render(request, 'dashboards.html',context)


@login_required
def view_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    return render(request, 'profile/view_profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    profile = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
@placement_required
def placement_dashboard(request):
    students = StudentProfile.objects.all()
    total_students = students.count()
    students_with_resume = students.exclude(resume='').count()
    students_without_resume = total_students - students_with_resume

    # Skills Analytics
    skill_counter = Counter()
    for student in students:
        if student.skills:
            skills = student.skills.split(',')
            for skill in skills:
                skill = skill.strip().lower()
                if skill:
                    skill_counter[skill] += 1
    top_skills = skill_counter.most_common(5)
    skill_labels = []
    skill_counts = []
    for skill, count in top_skills:
        skill_labels.append(skill.upper())
        skill_counts.append(count)

    # Job Role Analytics
    role_counter = Counter()
    for student in students:
        if student.preferred_job_role:
            roles = student.preferred_job_role.split(',')
            for role in roles:
                role = role.strip().lower()
                if role:
                    role_counter[role] += 1
    top_roles = role_counter.most_common(5)
    role_labels = []
    role_counts = []
    for role, count in top_roles:
        role_labels.append(role.upper())
        role_counts.append(count)

    return render(
        request,
        'placement/dashboard.html',
        {
            'total_students': total_students,
            'students_with_resume': students_with_resume,
            'students_without_resume': students_without_resume,
            'top_skills': top_skills,
            'top_roles': top_roles,
            'skill_labels': skill_labels,
            'skill_counts': skill_counts,
            'role_labels': role_labels,
            'role_counts': role_counts,
        }
    )


@login_required
@placement_required
def student_list(request):
    students = StudentProfile.objects.select_related('user')
    return render(request, 'placement/student_list.html', {'students': students})


@login_required
@placement_required
def student_detail(request, id):
    student = StudentProfile.objects.get(id=id)
    return render(request, 'placement/student_detail.html', {'student': student})


@login_required
def job_list(request):
    jobs = JobPosting.objects.all().order_by('-created_at')
    return render(request, 'placement/job_list.html', {'jobs': jobs})


@login_required
def apply_job(request, id):
    job = JobPosting.objects.get(id=id)
    student = StudentProfile.objects.get(user=request.user)
    already_applied = JobApplication.objects.filter(student=student, job=job).exists()
    if not already_applied:
        JobApplication.objects.create(student=student, job=job, status='Applied')
    return redirect(job.apply_link)


@login_required
def my_applications(request):
    student = StudentProfile.objects.get(user=request.user)
    applications = JobApplication.objects.filter(student=student)
    return render(request, 'placement/my_applications.html', {'applications': applications})


@login_required
@placement_required
def application_list(request):
    applications = JobApplication.objects.select_related('student', 'job')
    return render(request, 'placement/application_list.html', {'applications': applications})


@login_required
def update_status(request, id):
    application = JobApplication.objects.get(id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        return redirect('my_applications')
    return render(request, 'placement/update_status.html', {
        'application': application,
        'status_choices': JobApplication.STATUS_CHOICES
    })


@login_required

def student_dashboard(request):
    
    
    return render(request, 'accounts/student_dashboard.html', context)


@login_required
@placement_required
def create_job(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobPostingForm()
    return render(request, 'placement/create_job.html', {'form': form})


@login_required
def announcements(request):
    announcements = Announcement.objects.order_by('-created_at')
    return render(request, 'placement/announcements.html', {'announcements': announcements})


@login_required
@placement_required
def post_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('announcements')
        else:
            announcements = Announcement.objects.all()
            return render(request, 'placement/announcements.html', {'form': form, 'announcements': announcements})
    else:
        form = AnnouncementForm()
    announcements = Announcement.objects.all()
    return render(request, 'placement/announcements.html', {'form': form, 'announcements': announcements})


@login_required
def view_announcements(request):
    announcements = Announcement.objects.all()
    form = None
    return render(request, 'placement/announcements.html', {'announcements': announcements, 'form': form})