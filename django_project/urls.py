from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from accounts import views as account_views
from events.urls import router as events_router
from payments.urls import router as payments_router

router = DefaultRouter()

router.registry.extend(events_router.registry)
router.registry.extend(payments_router.registry)

router.register("accounts", account_views.CustomUserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include("events.urls")),
    path("", include("accounts.urls")),
    path("", include(router.urls)),
]