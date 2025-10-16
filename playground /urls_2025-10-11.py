from django.urls import path
from .views import ProxyAPIView, ApiRootView, ProxyAPIViewJSONXML, WMSJsonAPIView, WmsFetcher

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("proxy/", ProxyAPIView.as_view(), name="proxy-api"),
    path("proxyjsonxml/", ProxyAPIViewJSONXML.as_view(), name="proxysjonxml-api"),
    path("wms-json/", WMSJsonAPIView.as_view(), name="wms-json"),
    path("wms-fetcher/", WmsFetcher.as_view(), name="wms-fetcher"),
]

