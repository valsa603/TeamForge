from django.urls import path
from . import views


urlpatterns = [

    path(
        "create/",
        views.create_project,
        name="create_project"
    ),

    path(
        "my-projects/",
        views.project_list,
        name="project_list"
    ),

    path(
        "<int:project_id>/match/",
        views.match_teammates,
        name="match_teammates"
    ),

    path(
    "<int:project_id>/invite/<int:user_id>/",
    views.send_invitation,
    name="send_invitation"
),

    path(
         "invitations/",
         views.invitations,
         name="invitations"
),

path(
    "invitations/<int:invitation_id>/<str:action>/",
    views.respond_invitation,
    name="respond_invitation"
),
path(
    "<int:project_id>/workspace/",
    views.project_workspace,
    name="project_workspace"
),

path(
    "<int:project_id>/tasks/create/",
    views.create_task,
    name="create_task"
),

path(
    "tasks/<int:task_id>/status/",
    views.update_task_status,
    name="update_task_status"
),

path(
    "tasks/<int:task_id>/edit/",
    views.edit_task,
    name="edit_task"
),

path(
    "tasks/<int:task_id>/delete/",
    views.delete_task,
    name="delete_task"
),

path(
    "projects/<int:project_id>/add-member/",
    views.add_member,
    name="add_member"
),
path(
    "projects/<int:project_id>/remove-member/<int:user_id>/",
    views.remove_member,
    name="remove_member"
),

path(
    "my-tasks/",
    views.my_tasks,
    name="my_tasks"
),

path(
    "notifications/",
    views.notifications,
    name="notifications"
),
]