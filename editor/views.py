import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Path, Background, Point
from .forms import PathForm


def landing_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "editor/landing.html")


@login_required(login_url="login")
def dashboard_view(request):
    paths = Path.objects.filter(user=request.user)
    return render(request, "editor/dashboard.html", {"paths": paths})


def login_redirect(request):
    return redirect("login")  # Change to your custom login URL


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "editor/register.html", {"form": form})


@login_required(login_url="login")
def create_path(request):
    if request.method == "POST":
        form = PathForm(request.POST)
        if form.is_valid():
            path = form.save(commit=False)
            path.user = request.user
            path.save()
            return redirect("edit_path", path_id=path.id)
    else:
        form = PathForm()
    backgrounds = Background.objects.all()
    return render(
        request, "editor/create_path.html", {"form": form, "backgrounds": backgrounds}
    )


@login_required(login_url="login")
def edit_path(request, path_id):
    path = get_object_or_404(Path, id=path_id, user=request.user)

    if request.method == "POST":
        data = json.loads(request.POST.get("points", "[]"))
        path.points.all().delete()
        for i, point in enumerate(data):
            Point.objects.create(path=path, x=point["x"], y=point["y"], order=i)
        return redirect("display_path", path_id=path.id)

    points = list(path.points.values("x", "y").order_by("order"))
    return render(
        request,
        "editor/edit_path.html",
        {
            "path": path,
            "points_json": json.dumps(points),
            "background_url": path.background.image.url,
        },
    )


@login_required(login_url="login")
def display_path(request, path_id):
    path = get_object_or_404(Path, id=path_id)
    points_json = json.dumps(list(path.points.values("x", "y").order_by("order")))

    return render(
        request,
        "editor/display_path.html",
        {
            "path": path,
            "points_json": points_json,
            "background_url": path.background.image.url,
        },
    )


@login_required(login_url="login")
@require_http_methods(["POST"])
def delete_path(request, path_id):
    path = get_object_or_404(Path, id=path_id, user=request.user)
    path.delete()
    return redirect("dashboard")
