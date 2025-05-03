from rest_framework.authtoken import views as rest_auth_views
from rest_framework_nested import routers
from .views import PathViewSet, PointViewSet
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


# Define your schema view (Swagger)
schema_view = get_schema_view(
    openapi.Info(
        title="Pather API",
        default_version="v1",
        description="API for Pather provides the ability to perform CRUD operations on paths and points.",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

router = routers.SimpleRouter()
router.register(r"paths", PathViewSet, basename="paths")

paths_router = routers.NestedSimpleRouter(router, r"paths", lookup="path")
paths_router.register(r"points", PointViewSet, basename="path-points")

urlpatterns = [
    path("auth/", rest_auth_views.obtain_auth_token),
    path("", include(router.urls)),
    path("", include(paths_router.urls)),
    path(
        "doc/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
