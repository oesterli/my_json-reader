from django.urls import path
from .views import ProxyAPIView, ApiRootView, ProxyAPIViewJSONXML

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("proxy/", ProxyAPIView.as_view(), name="proxy-api"),
    path("proxyjsonxml/", ProxyAPIViewJSONXML.as_view(), name="proxysjonxml-api"),
]
