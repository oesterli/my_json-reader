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


class ProxyAPIViewJSONXML(APIView):
    """
    Proxy-Endpoint for external APIs.
    Supports JSON, XML und beliebige Query-Parameter.
    imports "fetch_wms_and_convert_to_json()" from .helpers

    Example call: http://127.0.0.1:8000/api/proxyjsonxml/?url=https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
    """

    def get(self, request):
        target_url = request.query_params.get("url")
        if not target_url:
            return Response({"error": "Parameter 'url' required!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Separate URL in Base + Query-Parameter
            parsed = urlparse(target_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            query_params = parse_qs(parsed.query)

            # parse_qs suuplies lists of values, convert to single strings
            query_params = {k: v[0] for k, v in query_params.items()}

            # Call external API
            resp = requests.get(base_url, params=query_params, timeout=15)
            resp.raise_for_status()

            # Check Content-Type
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return Response(resp.json(), status=resp.status_code)
            elif "xml" in content_type or resp.text.strip().startswith("<"):
                return HttpResponse(resp.text, content_type="application/xml", status=resp.status_code)
            else:
                # Fallback: Return text
                return HttpResponse(resp.text, content_type="text/plain", status=resp.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)


class WMSJsonAPIView(APIView):
    """
    Call WMS-Endpoint, save XML & JSON locally and return JSON
    imports "fetch_wms_and_convert_to_json()" from .helpers

    Example call: http://127.0.0.1:8000/api/wms-json/?url=https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
    """
    def get(self, request):
        target_url = request.query_params.get("url")
        if not target_url:
            return Response({"error": "Parameter 'url' fehlt"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_dict, xml_path, json_path = fetch_wms_and_convert_to_json(target_url)
            return Response({
                "message": "WMS erfolgreich abgerufen und konvertiert",
                "xml_file": xml_path,
                "json_file": json_path,
                "data": data_dict
            })
        except RuntimeError as e:
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
        
        

