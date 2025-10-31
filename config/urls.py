from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def home_view(request):
    return HttpResponse("Добро пожаловать в сеть поставок!")


urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("network_link.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
