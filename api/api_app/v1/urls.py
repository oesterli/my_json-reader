from django.urls import path
from .views import ProxyAPIView, ApiRootView, WmsFetcher

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("catalog/", ProxyAPIView.as_view(), name="catalog-fetcher"),
    path("wms/", WmsFetcher.as_view(), name="wms-fetcher"),
]

