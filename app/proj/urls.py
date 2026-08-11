import os

from django.contrib import admin
from django.urls import include, path

from demo import views

PKG = os.environ.get("PKG", "silk")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index),
    path("secretish/", views.secretish),
]

if PKG == "silk":
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
elif PKG == "debug_toolbar":
    from django.conf import settings as _s
    from django.http import JsonResponse

    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
    urlpatterns.append(
        path(
            "whoami/",
            lambda r: JsonResponse(
                {
                    "REMOTE_ADDR": r.META.get("REMOTE_ADDR"),
                    "HTTP_X_FORWARDED_FOR": r.META.get("HTTP_X_FORWARDED_FOR"),
                    "INTERNAL_IPS": list(getattr(_s, "INTERNAL_IPS", [])),
                    "DEBUG": _s.DEBUG,
                }
            ),
        )
    )
elif PKG == "health_check":
    import importlib.util

    if importlib.util.find_spec("health_check.urls") is not None:
        # 3.x quickstart
        urlpatterns.append(path("ht/", include("health_check.urls")))
    else:
        # 4.x quickstart
        from health_check.views import HealthCheckView

        urlpatterns.append(path("ht/", HealthCheckView.as_view(), name="health_check"))
elif PKG == "prometheus":
    urlpatterns.append(path("", include("django_prometheus.urls")))
elif PKG == "spectacular":
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )
    from rest_framework import routers

    from demo import api as demo_api

    router = routers.DefaultRouter()
    router.register("notes", demo_api.NoteViewSet)
    router.register("internal/users", demo_api.InternalUserViewSet)
    router.register("internal/billing", demo_api.InternalBillingViewSet, basename="billing")

    urlpatterns += [
        path("api/", include(router.urls)),
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
        ),
        path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema")),
    ]
elif PKG == "graphene":
    from graphene_django.views import GraphQLView

    urlpatterns.append(path("graphql", GraphQLView.as_view(graphiql=True)))
elif PKG == "yasg":
    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view
    from rest_framework import routers

    from demo import api as demo_api

    router = routers.DefaultRouter()
    router.register("notes", demo_api.NoteViewSet)
    router.register("internal/users", demo_api.InternalUserViewSet)
    router.register("internal/billing", demo_api.InternalBillingViewSet, basename="billing")

    # Copied verbatim from the drf-yasg README quickstart.
    schema_view = get_schema_view(
        openapi.Info(title="Demo API", default_version="v1"),
        public=True,
    )

    urlpatterns += [
        path("api/", include(router.urls)),
        path(
            "swagger<format>",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
elif PKG == "rq":
    urlpatterns.append(path("django-rq/", include("django_rq.urls")))
elif PKG == "explorer":
    urlpatterns.append(path("explorer/", include("explorer.urls")))
