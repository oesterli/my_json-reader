from django.shortcuts import render

# Create your views here.

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class ProxyAPIView(APIView):
    """
    Nimmt eine externe URL entgegen, ruft die API ab
    und gibt die JSON-Antwort zurück.
    """

    def get(self, request):
        target_url = request.query_params.get("url")
        if not target_url:
            return Response(
                {"error": "Parameter 'url' ist erforderlich"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            response = requests.get(target_url, timeout=10)
            response.raise_for_status()
            return Response(response.json(), status=response.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        

class ApiRootView(APIView):
    """
    Gibt eine einfache Willkommens-Nachricht für die Basis-URL /api/ zurück.
    """
    def get(self, request):
        return Response({"message": "Willkommen bei der Basis-URL der API!"})

