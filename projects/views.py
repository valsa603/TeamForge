from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Project, Invitation,Task,Notification
from .forms import ProjectForm, TaskForm
from accounts.models import Profile


@login_required
def create_project(request):

    if request.method == "POST":

        form = ProjectForm(request.POST)

        if form.is_valid():

            project = form.save(commit=False)

            project.creator = request.user

            project.save()

            form.save_m2m()

            project.members.add(request.user)

            return redirect("project_list")

    else:

        form = ProjectForm()

    return render(
        request,
        "create_project.html",
        {"form": form}
    )


@login_required
def project_list(request):

    
 projects = Project.objects.filter(
    Q(creator=request.user) | Q(members=request.user)
).distinct()
 return render(
        request,
        "project_list.html",
        {"projects": projects}
    )

@login_required
def match_teammates(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id,
        creator=request.user
    )

    required_skills = set(
        project.required_skills.all()
    )

    candidates = Profile.objects.exclude(
        user__in=project.members.all()
    ).exclude(
        user=project.creator
    ).prefetch_related(
        "skills",
        "user"
    )

    recommendations = []

    for profile in candidates:

        student_skills = set(
            profile.skills.all()
        )

        matched_skills = (
            required_skills.intersection(
                student_skills
            )
        )

        if required_skills:

            score = round(
                (len(matched_skills) /
                 len(required_skills)) * 100
            )

        else:

            score = 0

        if score > 0:

            recommendations.append({
                "profile": profile,
                "score": score,
                "matched_skills": matched_skills,
            })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return render(
        request,
        "match_teammates.html",
        {
            "project": project,
            "recommendations": recommendations,
        }
    )

@login_required
def send_invitation(request, project_id, user_id):

    if request.method != "POST":
        return redirect("match_teammates", project_id=project_id)

    project = get_object_or_404(
        Project,
        id=project_id,
        creator=request.user
    )

    invitee = get_object_or_404(
        User,
        id=user_id
    )

    # Don't invite yourself
    if invitee == request.user:
        return redirect(
            "match_teammates",
            project_id=project.id
        )

    # Don't invite someone already in the team
    if project.members.filter(
        id=invitee.id
    ).exists():

        return redirect(
            "match_teammates",
            project_id=project.id
        )

    # Don't invite if team is already full
    if project.members.count() >= project.team_size:

        return redirect(
            "match_teammates",
            project_id=project.id
        )

    # Don't create duplicate pending invitations
    existing = Invitation.objects.filter(
        project=project,
        invitee=invitee,
        status="pending"
    ).exists()

    if not existing:

        Invitation.objects.create(
            project=project,
            inviter=request.user,
            invitee=invitee
        )

    return redirect(
        "match_teammates",
        project_id=project.id
    )

@login_required
def invitations(request):

    invitation_list = Invitation.objects.filter(
        invitee=request.user,
        status="pending"
    ).select_related(
        "project",
        "inviter"
    )

    return render(
        request,
        "invitations.html",
        {
            "invitations": invitation_list
        }
    )

@login_required
def respond_invitation(
    request,
    invitation_id,
    action
):

    invitation = get_object_or_404(
        Invitation,
        id=invitation_id,
        invitee=request.user,
        status="pending"
    )

    if request.method != "POST":
        return redirect("invitations")

    if action == "accepted":

        project = invitation.project

        if project.members.count() < project.team_size:

            project.members.add(request.user)

            invitation.status = "accepted"

            invitation.save()

        else:

            # Team is already full
            invitation.status = "rejected"

            invitation.save()

    elif action == "rejected":

        invitation.status = "rejected"

        invitation.save()

    return redirect("invitations")

@login_required
@login_required
def project_workspace(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Only project members can access
    if not project.members.filter(
        id=request.user.id
    ).exists():
        return redirect("project_list")

    members = project.members.all()

    tasks = project.tasks.all()

    total_tasks = tasks.count()

    completed_tasks = tasks.filter(
        status="completed"
    ).count()

    progress = 0

    if total_tasks > 0:
        progress = int(
            (completed_tasks / total_tasks) * 100
        )

    return render(
        request,
        "project_workspace.html",
        {
            "project": project,
            "members": members,
            "tasks": tasks,
            "progress": progress,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
        }
    )
@login_required
def create_task(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    # Only team members can create tasks
    if not project.members.filter(
        id=request.user.id
    ).exists():

        return redirect("project_list")

    if request.method == "POST":

        form = TaskForm(request.POST)

        # Only show project members
        form.fields["assigned_to"].queryset = (
            project.members.all()
        )

        if form.is_valid():

            task = form.save(commit=False)

            task.project = project

            task.save()
            Notification.objects.create(
    recipient=task.assigned_to,
    message=f"You have been assigned a new task: {task.title}"
)

            return redirect(
                "project_workspace",
                project_id=project.id
            )

    else:

        form = TaskForm()

        form.fields["assigned_to"].queryset = (
            project.members.all()
        )

    return render(
        request,
        "create_task.html",
        {
            "form": form,
            "project": project,
        }
    )

@login_required
def update_task_status(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    # Only project members can update tasks
    if not task.project.members.filter(id=request.user.id).exists():
        return redirect("project_list")

    if request.method == "POST":
        new_status = request.POST.get("status")

        if new_status in ["todo", "progress", "completed"]:
            task.status = new_status
            task.save()

    return redirect(
        "project_workspace",
        project_id=task.project.id
    )
@login_required
def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if not task.project.members.filter(id=request.user.id).exists():
        return redirect("project_list")

    if request.method == "POST":

        form = TaskForm(request.POST, instance=task)

        form.fields["assigned_to"].queryset = (
            task.project.members.all()
        )

        if form.is_valid():
            form.save()

            return redirect(
                "project_workspace",
                project_id=task.project.id
            )

    else:

        form = TaskForm(instance=task)

        form.fields["assigned_to"].queryset = (
            task.project.members.all()
        )

    return render(
        request,
        "edit_task.html",
        {
            "form": form,
            "task": task,
        }
    )

@login_required
def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    project_id = task.project.id

    if not task.project.members.filter(id=request.user.id).exists():
        return redirect("project_list")

    if request.method == "POST":
        task.delete()

        return redirect(
            "project_workspace",
            project_id=project_id
        )

    return render(
        request,
        "delete_task.html",
        {
            "task": task,
        }
    )

@login_required
def add_member(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Only project creator can add members
    if request.user != project.creator:
        return redirect("project_workspace", project_id=project.id)

    if request.method == "POST":
        username = request.POST.get("username")

        try:
            user = User.objects.get(username=username)
            project.members.add(user)
        except User.DoesNotExist:
            pass

    return redirect("project_workspace", project_id=project.id)

@login_required
def remove_member(request, project_id, user_id):
    project = get_object_or_404(Project, id=project_id)

    # Only project creator can remove members
    if request.user != project.creator:
        return redirect("project_workspace", project_id=project.id)

    user = get_object_or_404(User, id=user_id)

    project.members.remove(user)

    return redirect("project_workspace", project_id=project.id)

@login_required
def project_list(request):

    search_query = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    projects = Project.objects.filter(
        creator=request.user
    )

    if search_query:
        projects = projects.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(required_skills__name__icontains=search_query)
        ).distinct()

    if status_filter:
        projects = projects.filter(
            status=status_filter
        )

    return render(
        request,
        "project_list.html",
        {
            "projects": projects,
            "search_query": search_query,
            "status_filter": status_filter,
        }
    )

@login_required
def my_tasks(request):

    tasks = Task.objects.filter(
        assigned_to=request.user
    ).select_related(
        "project",
        "assigned_to"
    )

    return render(
        request,
        "my_tasks.html",
        {
            "tasks": tasks
        }
    )

@login_required
def notifications(request):

    notification_list = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    return render(
        request,
        "notifications.html",
        {
            "notifications": notification_list
        }
    )