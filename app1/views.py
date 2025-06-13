from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm
from django.core.mail import send_mail
from django.http import HttpResponseForbidden

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-id')
    applications = JobApplication.objects.filter(job__posted_by=request.user).order_by('-id')
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs , 'applications': applications})

@login_required
def create_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_dashboard')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form})

@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, posted_by=request.user)
    if request.method == 'POST':
        job.delete()
        return redirect('employer_dashboard')
    return render(request, 'jobs/confirm_delete.html', {'job': job})

def jobs_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/jobs_list.html', {'jobs': jobs})

def job_details(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'jobs/job_details.html', {'job': job})

@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            # Optional: Email to employer
            send_mail(
                f'New Application for {job.title}',
                f'{request.user.username} applied.',
                from_email=None,
                recipient_list=[job.posted_by.email],
                fail_silently=True
            )
            return redirect('job_seeker_dashboard')
    else:
        form = JobApplicationForm()
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
def job_seeker_dashboard(request):
    applications = JobApplication.objects.filter(applicant=request.user).order_by('-id')
    return render(request, 'jobs/seeker_dashboard.html', {'applications': applications})

@login_required
def edit_application(request, app_id):
    app = get_object_or_404(JobApplication, id=app_id, applicant=request.user)
    if app.status != 'pending':
        return HttpResponseForbidden("Can't edit this application.")
    form = JobApplicationForm(request.POST or None, request.FILES or None, instance=app)
    if form.is_valid():
        form.save()
        return redirect('job_seeker_dashboard')
    return render(request, 'jobs/edit_application.html', {'form': form})

@login_required
def delete_application(request, app_id):
    app = get_object_or_404(JobApplication, id=app_id, applicant=request.user)
    if app.status != 'pending':
        return HttpResponseForbidden("Can't delete this application.")
    if request.method == 'POST':
        app.delete()
        return redirect('job_seeker_dashboard')
    return render(request, 'jobs/confirm_delete_application.html', {'application': app})

@login_required
def update_application_status(request, app_id, new_status):
    app = get_object_or_404(JobApplication, id=app_id)
    # if app.job.posted_by != request.user:
    #     return redirect('employer_dashboard')
    if new_status in ['accepted', 'rejected']:
        app.status = new_status
        app.save()
        send_mail(
            f"Your Application to {app.job.title}",
            f"Status: {new_status.upper()}",
            from_email=None,
            recipient_list=[app.applicant.email],
            fail_silently=True
        )
    return redirect('employer_dashboard')