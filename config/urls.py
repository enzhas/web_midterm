from django.urls import include, path
from tours.views import api_root
urlpatterns = [path("", api_root), path("api/", include("tours.urls"))]
handler404 = "tours.views.not_found"
handler500 = "tours.views.server_error"
