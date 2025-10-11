from django.urls import path, include

urlpatterns = [
    path("v1/", include("api_app.v1.urls")),
]

