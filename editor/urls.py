from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="editor/login.html", redirect_authenticated_user=True
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="landing"), name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_path, name="create_path"),
    path("path<int:path_id>/", views.display_path, name="display_path"),
    path("path<int:path_id>-edit/", views.edit_path, name="edit_path"),
    path("path<int:path_id>/delete/", views.delete_path, name="delete_path"),
]
