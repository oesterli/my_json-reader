from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .api_functions import fetch_wmts_wms_save_response # WmsFetcher
from .api_functions import fetch_catalog_save_response # ProxyAPIView

# -------------------------
class ApiRootView(APIView):
    """
    Returns a welcome message when calling /api/
    Example call: http://127.0.0.1:8000/api/v1/
    """
    def get(self, request):
        try:
            message = {"message": "Welcome! This is the base URL of the API"}
            return Response(message, status=status.HTTP_200_OK)
        except Exception as e:
            message = {"error": f"Unecpected error: {str(e)}"}
            return Response(message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -------------------------
class CatalogApiView(APIView):
    """
    Saves Catalog service
    imports "fetch_catalog_save_response()" from .api_functions.py
    Example call: http://127.0.0.1:8000/api/v1/catalog/
    """
    def get(self, request):
        try:
            result = fetch_catalog_save_response()

            if result["errors"]:
                return Response({
                    "message": "Errors occurred",
                    "saved_files": result["saved_files"],
                    "errors": result["errors"]
                }, status=status.HTTP_502_BAD_GATEWAY)

            return Response({
                "message": "Done",
                "saved_files": result["saved_files"]
            })

        except Exception as e:
            # Fallback für unerwartete Fehler in der View selbst
            return Response({
                "message": "Unexpected error in view",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# -------------------------
class WmsApiView(APIView):
    """
    Saves WMS, WMTS
    imports "ffetch_wmts_wms_save_response()" from .api_functions.py
    Example call: http://127.0.0.1:8000/api/v1/wms/
    """
    def get(self, request):
        try:
            result = fetch_wmts_wms_save_response()

            if result["errors"]:
                return Response({
                    "message": "Errors occurred",
                    "saved_files": result["saved_files"],
                    "errors": result["errors"]
                }, status=status.HTTP_502_BAD_GATEWAY)


            return Response({
                    "message": "Done",
                    "saved_files": result["saved_files"],
                })
        
        except Exception as e:
            return Response({
                "message": "Unexpected error in view",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

