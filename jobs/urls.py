from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("add-job/", views.add_job, name="add_job"),

    path("applications/", views.job_list, name="job_list"),

    path(
        "job/<int:job_id>/",
        views.job_detail,
        name="job_detail"
    ),

    path(
        "edit-job/<int:job_id>/",
        views.edit_job,
        name="edit_job"
    ),

    path(
        "delete-job/<int:job_id>/",
        views.delete_job,
        name="delete_job"
    ),

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
    "login/",
    views.user_login,
    name="login"
    ),  

    path(
    "logout/",
    views.user_logout,
    name="logout"
    ),

    path(
    "job/<int:job_id>/update-status/",
    views.update_status,
    name="update_status"
    ),


]