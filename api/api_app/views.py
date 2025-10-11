from django.shortcuts import render

# Create your views here.

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import HttpResponse # For ProxyAPIViewJSONXML
from urllib.parse import urlparse, parse_qs # For ProxyAPIViewJSONXML

from .helpers import fetch_wms_and_convert_to_json # WMSJsonAPIView

from api_app.helpers import fetch_and_save_wms_xml # WmsFetcher


class ApiRootView(APIView):
    """
    Returns a welcom message when calling /api/
    
    Example call: http://127.0.0.1:8000/api/
    """
    def get(self, request):
        return Response({"message": "Welcome! This is the base URL of the API"})

class ProxyAPIView(APIView):
    """
    Call the API with an external URL als url-parameter "url" and return a JSON
    
    Example call: http://127.0.0.1:8000/api/proxy/?url=https://jsonplaceholder.typicode.com/todos/1
    """

    def get(self, request):
        target_url = request.query_params.get("url")
        if not target_url:
            return Response(
                {"error": "Parameter 'url' required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.get(target_url, timeout=10)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class WmsFetcher(APIView):
    """
    Saves WMS, WMTS
    imports "fetch_and_save_wms_xml()" from .helpers

    Example call: http://127.0.0.1:8000/api/wms-fetcher/
    """
    # est = xml_path, json_path, data_dict

    def get(self, request):
    
        xml, json, *rest = fetch_and_save_wms_xml()
        # print(f"XML gespeichert unter: {file_path}")

        return Response({
                "message": "Done",
                "xml": xml,
                "json": json

            })
        
        

