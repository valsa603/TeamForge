from django.contrib import admin
from django.urls import path, include
from projects import views


urlpatterns = [

    path("admin/", admin.site.urls),

    path("", include("accounts.urls")),

    path(
        "projects/",
        include("projects.urls")
    ),

    path("my-tasks/", views.my_tasks, name="my_tasks"),

]