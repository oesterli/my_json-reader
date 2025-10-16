from django.urls import path
from .views import CatalogApiView, ApiRootView, WmsApiView

urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("catalog/", CatalogApiView.as_view(), name="catalog-fetcher"),
    path("wms/", WmsApiView.as_view(), name="wms-fetcher"),
]

