from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from editor import views as editor_views

urlpatterns = [
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('', editor_views.landing_view, name='landing'),
    path('login/', auth_views.LoginView.as_view(
        template_name='editor/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('register/', editor_views.register, name='register'),
    path('editor/', include('editor.urls')),
    path('accounts/login/', editor_views.login_redirect, name='login_redirect'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
