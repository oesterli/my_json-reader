from django.shortcuts import render

# Create your views here.

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .helpers import fetch_service_save_xml_json # WmsFetcher

from .helpers import get_json # ProxyAPIView


class ApiRootView(APIView):
    """
    Returns a welcom message when calling /api/
    
    Example call: http://127.0.0.1:8000/api/v1/
    """
    def get(self, request):
        return Response({"message": "Welcome! This is the base URL of the API"})


class ProxyAPIView(APIView):
    """
    Saves Catalog service
    imports "get_json()" from .helpers
    
    Example call: http://127.0.0.1:8000/api/v1/proxy/
    """

    def get(self, request):
        try:
       
            # Call helper function
            catalog = get_json()

            return Response({
                "message": "Done",
                "catalog": catalog
             })
        except:
            return Response({
                "message": "Error! Something went wrong"
             })


class WmsFetcher(APIView):
    """
    Saves WMS, WMTS
    imports "fetch_service_save_xml_json()" from .helpers

    Example call: http://127.0.0.1:8000/api/v1/wms-fetcher/
    """
    # est = xml_path, json_path, data_dict

    def get(self, request):
    
        xml, json, *rest = fetch_service_save_xml_json()

        return Response({
                "message": "Done",
                "xml": xml,
                "json": json

            })
        
        

