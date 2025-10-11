from django.urls import path
from .views import ProxyAPIView, ApiRootView, WmsFetcher

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("proxy/", ProxyAPIView.as_view(), name="proxy-api"),
    path("wms-fetcher/", WmsFetcher.as_view(), name="wms-fetcher"),
]

