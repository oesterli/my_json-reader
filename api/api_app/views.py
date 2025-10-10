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







from django.http import HttpResponse
from urllib.parse import urlparse, parse_qs


class ProxyAPIViewJSONXML(APIView):
    """
    Proxy-Endpoint für externe APIs.
    Unterstützt JSON, XML und beliebige Query-Parameter.
    """

    def get(self, request):
        target_url = request.query_params.get("url")
        if not target_url:
            return Response({"error": "Parameter 'url' ist erforderlich"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # URL in Basis + Query-Parameter aufteilen
            parsed = urlparse(target_url)
            base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            query_params = parse_qs(parsed.query)

            # parse_qs liefert Listen als Werte, convertiere zu einzelnen Strings
            query_params = {k: v[0] for k, v in query_params.items()}

            # Externe API aufrufen
            resp = requests.get(base_url, params=query_params, timeout=15)
            resp.raise_for_status()

            # Content-Type prüfen
            content_type = resp.headers.get("Content-Type", "")
            if "json" in content_type:
                return Response(resp.json(), status=resp.status_code)
            elif "xml" in content_type or resp.text.strip().startswith("<"):
                return HttpResponse(resp.text, content_type="application/xml", status=resp.status_code)
            else:
                # Fallback: Text zurückgeben
                return HttpResponse(resp.text, content_type="text/plain", status=resp.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
