from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models.functions import TruncMonth
from datetime import date

from .forms import JobApplicationForm
from .models import JobApplication, ApplicationStatusHistory


# =========================================================
# Helper Function - Calculate Deadline Status
# =========================================================

def calculate_deadline_status(job):
    """
    Calculate deadline information for a job.
    """

    if job.deadline is None:
        job.days_left = None
        job.deadline_status = "No deadline"
        job.deadline_status_class = "secondary"
        return job

    today = timezone.localdate()

    days_left = (job.deadline - today).days

    job.days_left = days_left

    # =====================================================
    # OVERDUE
    # =====================================================

    if days_left < 0:

        overdue_days = abs(days_left)

        if overdue_days == 1:
            job.deadline_status = "Overdue by 1 day"
        else:
            job.deadline_status = (
                f"Overdue by {overdue_days} days"
            )

        job.deadline_status_class = "danger"

    # =====================================================
    # DUE TODAY
    # =====================================================

    elif days_left == 0:

        job.deadline_status = "Due today"
        job.deadline_status_class = "danger"

    # =====================================================
    # ONE DAY LEFT
    # =====================================================

    elif days_left == 1:

        job.deadline_status = "1 day left"
        job.deadline_status_class = "warning"

    # =====================================================
    # MORE THAN ONE DAY LEFT
    # =====================================================

    else:

        job.deadline_status = (
            f"{days_left} days left"
        )

        if days_left <= 7:
            job.deadline_status_class = "warning"
        else:
            job.deadline_status_class = "success"

    return job


# =========================================================
# Monthly Application Analytics
# =========================================================

def get_monthly_application_analytics(user_jobs):
    """
    Generate application statistics for the last 12 months.

    The analytics are based on application_date.

    Returns a list containing:

        month
        month_name
        Applied
        Interview
        Offer
        Accepted
        Rejected
        total
    """

    today = timezone.localdate()

    # -----------------------------------------------------
    # First day of the current month
    # -----------------------------------------------------

    current_month = today.replace(day=1)

    # -----------------------------------------------------
    # Calculate date 11 months before current month
    # -----------------------------------------------------

    year = current_month.year
    month = current_month.month - 11

    while month <= 0:
        month += 12
        year -= 1

    start_date = date(
        year,
        month,
        1
    )

    # -----------------------------------------------------
    # Get applications grouped by month
    # -----------------------------------------------------

    monthly_data = (
        user_jobs
        .filter(
            application_date__gte=start_date
        )
        .annotate(
            month=TruncMonth(
                "application_date"
            )
        )
        .values(
            "month"
        )
        .annotate(
            total=Count("id"),
            applied=Count(
                "id",
                filter=Q(status="Applied")
            ),
            interview=Count(
                "id",
                filter=Q(status="Interview")
            ),
            offer=Count(
                "id",
                filter=Q(status="Offer")
            ),
            accepted=Count(
                "id",
                filter=Q(status="Accepted")
            ),
            rejected=Count(
                "id",
                filter=Q(status="Rejected")
            )
        )
        .order_by("month")
    )

    # -----------------------------------------------------
    # Convert QuerySet into dictionary
    # -----------------------------------------------------

    monthly_lookup = {}

    for item in monthly_data:

        month_value = item["month"]

        if hasattr(month_value, "date"):
            month_value = month_value.date()

        month_key = month_value.strftime(
            "%Y-%m"
        )

        monthly_lookup[month_key] = item

    # -----------------------------------------------------
    # Build all 12 months
    # -----------------------------------------------------

    analytics = []

    current_year = current_month.year
    current_month_number = current_month.month

    for i in range(12):

        month_number = current_month_number - (11 - i)
        month_year = current_year

        while month_number <= 0:
            month_number += 12
            month_year -= 1

        month_date = date(
            month_year,
            month_number,
            1
        )

        month_key = month_date.strftime(
            "%Y-%m"
        )

        data = monthly_lookup.get(
            month_key
        )

        if data:

            analytics.append({
                "month": month_key,
                "month_name": month_date.strftime(
                    "%b %Y"
                ),
                "total": data["total"],
                "applied": data["applied"],
                "interview": data["interview"],
                "offer": data["offer"],
                "accepted": data["accepted"],
                "rejected": data["rejected"],
            })

        else:

            analytics.append({
                "month": month_key,
                "month_name": month_date.strftime(
                    "%b %Y"
                ),
                "total": 0,
                "applied": 0,
                "interview": 0,
                "offer": 0,
                "accepted": 0,
                "rejected": 0,
            })

    return analytics


# =========================================================
# Dashboard
# =========================================================

@login_required
def home(request):

    # Get only logged-in user's applications
    user_jobs = JobApplication.objects.filter(
        user=request.user
    )

    # =====================================================
    # Total Applications
    # =====================================================

    total_jobs = user_jobs.count()

    # =====================================================
    # Status Counts
    # =====================================================

    applied_count = user_jobs.filter(
        status="Applied"
    ).count()

    interview_count = user_jobs.filter(
        status="Interview"
    ).count()

    offer_count = user_jobs.filter(
        status="Offer"
    ).count()

    accepted_count = user_jobs.filter(
        status="Accepted"
    ).count()

    rejected_count = user_jobs.filter(
        status="Rejected"
    ).count()

    # =====================================================
    # Application Insights
    # =====================================================

    if total_jobs > 0:

        interview_rate = round(
            (interview_count / total_jobs) * 100,
            1
        )

        offer_rate = round(
            (offer_count / total_jobs) * 100,
            1
        )

        acceptance_rate = round(
            (accepted_count / total_jobs) * 100,
            1
        )

    else:

        interview_rate = 0
        offer_rate = 0
        acceptance_rate = 0

    # =====================================================
    # Deadline Management
    # =====================================================

    today = timezone.localdate()

    # -----------------------------------------------------
    # Upcoming Deadline Count
    # -----------------------------------------------------

    upcoming_deadline_count = user_jobs.filter(
        deadline__gte=today,
        deadline__isnull=False
    ).count()

    # -----------------------------------------------------
    # Overdue Deadline Count
    # -----------------------------------------------------

    overdue_deadline_count = user_jobs.filter(
        deadline__lt=today,
        deadline__isnull=False
    ).count()

    # -----------------------------------------------------
    # Upcoming Deadlines
    # -----------------------------------------------------

    upcoming_deadlines = user_jobs.filter(
        deadline__gte=today,
        deadline__isnull=False
    ).order_by(
        "deadline"
    )[:5]

    for job in upcoming_deadlines:
        calculate_deadline_status(job)

    # -----------------------------------------------------
    # Overdue Deadlines
    # -----------------------------------------------------

    overdue_deadlines = user_jobs.filter(
        deadline__lt=today,
        deadline__isnull=False
    ).order_by(
        "-deadline"
    )[:5]

    for job in overdue_deadlines:
        calculate_deadline_status(job)

    # =====================================================
    # Recent Applications
    # =====================================================

    recent_jobs = user_jobs.order_by(
        "-created_at"
    )[:5]

    for job in recent_jobs:
        calculate_deadline_status(job)

    # =====================================================
    # MONTHLY ANALYTICS
    # =====================================================

    monthly_analytics = get_monthly_application_analytics(
        user_jobs
    )

    # =====================================================
    # Context
    # =====================================================

    context = {

        # Application statistics
        "total_jobs": total_jobs,
        "applied_count": applied_count,
        "interview_count": interview_count,
        "offer_count": offer_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,

        # Application insights
        "interview_rate": interview_rate,
        "offer_rate": offer_rate,
        "acceptance_rate": acceptance_rate,

        # Deadline information
        "upcoming_deadline_count": upcoming_deadline_count,
        "overdue_deadline_count": overdue_deadline_count,
        "upcoming_deadlines": upcoming_deadlines,
        "overdue_deadlines": overdue_deadlines,

        # Recent applications
        "recent_jobs": recent_jobs,

        # Monthly analytics
        "monthly_analytics": monthly_analytics,

        # Today's date
        "today": today,
    }

    return render(
        request,
        "jobs/home.html",
        context
    )


# =========================================================
# Add Job
# =========================================================

@login_required
def add_job(request):

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST
        )

        if form.is_valid():

            job = form.save(
                commit=False
            )

            job.user = request.user

            job.save()

            ApplicationStatusHistory.objects.create(
                job_application=job,
                status=job.status
            )

            return redirect(
                "home"
            )

    else:

        form = JobApplicationForm()

    return render(
        request,
        "jobs/add_job.html",
        {
            "form": form
        }
    )


# =========================================================
# Job List
# =========================================================

@login_required
def job_list(request):

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    status_filter = request.GET.get(
        "status",
        ""
    )

    sort_by = request.GET.get(
        "sort",
        "newest"
    )

    jobs = JobApplication.objects.filter(
        user=request.user
    )

    # =====================================================
    # Search
    # =====================================================

    if search_query:

        jobs = jobs.filter(
            Q(
                company_name__icontains=search_query
            )
            |
            Q(
                job_title__icontains=search_query
            )
        )

    # =====================================================
    # Status Filter
    # =====================================================

    if status_filter:

        jobs = jobs.filter(
            status=status_filter
        )

    # =====================================================
    # Sorting
    # =====================================================

    if sort_by == "oldest":

        jobs = jobs.order_by(
            "created_at"
        )

    elif sort_by == "company_asc":

        jobs = jobs.order_by(
            "company_name"
        )

    elif sort_by == "company_desc":

        jobs = jobs.order_by(
            "-company_name"
        )

    elif sort_by == "date_newest":

        jobs = jobs.order_by(
            "-application_date"
        )

    elif sort_by == "date_oldest":

        jobs = jobs.order_by(
            "application_date"
        )

    else:

        jobs = jobs.order_by(
            "-created_at"
        )

    # =====================================================
    # Pagination
    # =====================================================

    paginator = Paginator(
        jobs,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    # =====================================================
    # Deadline Status
    # =====================================================

    for job in page_obj:
        calculate_deadline_status(job)

    today = timezone.localdate()

    # =====================================================
    # Context
    # =====================================================

    context = {

        "jobs": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "status_filter": status_filter,
        "sort_by": sort_by,
        "today": today,
    }

    return render(
        request,
        "jobs/job_list.html",
        context
    )


# =========================================================
# Job Detail
# =========================================================

@login_required
def job_detail(request, job_id):

    job = get_object_or_404(
        JobApplication,
        id=job_id,
        user=request.user
    )

    calculate_deadline_status(job)

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job
        }
    )


# =========================================================
# Edit Job
# =========================================================

@login_required
def edit_job(request, job_id):

    job = get_object_or_404(
        JobApplication,
        id=job_id,
        user=request.user
    )

    if request.method == "POST":

        form = JobApplicationForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            return redirect(
                "job_list"
            )

    else:

        form = JobApplicationForm(
            instance=job
        )

    return render(
        request,
        "jobs/edit_job.html",
        {
            "form": form,
            "job": job
        }
    )


# =========================================================
# Delete Job
# =========================================================

@login_required
def delete_job(request, job_id):

    job = get_object_or_404(
        JobApplication,
        id=job_id,
        user=request.user
    )

    if request.method == "POST":

        job.delete()

        return redirect(
            "job_list"
        )

    return render(
        request,
        "jobs/delete_job.html",
        {
            "job": job
        }
    )


# =========================================================
# Register
# =========================================================

def register(request):

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user
            )

            return redirect(
                "home"
            )

    else:

        form = UserCreationForm()

    return render(
        request,
        "jobs/register.html",
        {
            "form": form
        }
    )


# =========================================================
# Login
# =========================================================

def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(
                request,
                user
            )

            return redirect(
                "home"
            )

    else:

        form = AuthenticationForm()

    return render(
        request,
        "jobs/login.html",
        {
            "form": form
        }
    )


# =========================================================
# Logout
# =========================================================

def user_logout(request):

    logout(request)

    return redirect(
        "login"
    )


# =========================================================
# Update Status
# =========================================================

@login_required
def update_status(request, job_id):

    job = get_object_or_404(
        JobApplication,
        id=job_id,
        user=request.user
    )

    if request.method == "POST":

        new_status = request.POST.get(
            "status"
        )

        valid_statuses = [
            "Applied",
            "Interview",
            "Rejected",
            "Offer",
            "Accepted",
        ]

        if new_status in valid_statuses:

            old_status = job.status

            if old_status != new_status:

                job.status = new_status

                job.save()

                ApplicationStatusHistory.objects.create(
                    job_application=job,
                    status=new_status
                )

    return redirect(
        "job_detail",
        job_id=job.id
    )