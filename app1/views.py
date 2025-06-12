from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import JobForm

@login_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user).order_by('-id')
    return render(request, 'jobs/dashboard.html', {'jobs': jobs})

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
