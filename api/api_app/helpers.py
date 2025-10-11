import requests
import xmltodict
import os
import json
import re

def fetch_and_save_wms_xml(
    save_dir="tmp",
    xml_filename="service_response.xml",
    json_filename="service_response.json"
):
    """
    Ruft eine fest hinterlegte WMS-URL ab und speichert die Response als XML-Datei.
    """

    # Deine WMS-URL (hartkodiert)
    wms_url = "https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities"
    wmts_url = "https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml"

    urls = [wms_url, wmts_url]

    # Speicherordner anlegen
    os.makedirs(save_dir, exist_ok=True)
    # xml_path = os.path.join(save_dir, xml_filename)
    # json_path = os.path.join(save_dir, json_filename)

    try:
        for url in urls:
            print(url)

            match = re.search(r"^https://([^\.]+)\.", url)
            if match:
                typ = match.group(1)  # speichert "wms" bzw. "wmts"
                print(typ)

            xml_path = os.path.join(save_dir, f'{typ}.xml')
            json_path = os.path.join(save_dir,  f'{typ}.json')

            # Request an den WMS-Server
            # response = requests.get(wms_url, timeout=20)
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            # Response als XML speichern
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            # XML in Python-Dict konvertieren
            data_dict = xmltodict.parse(response.text)

            # JSON speichern
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=2)    

        return xml_path, json_path, data_dict

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Fehler beim Abrufen der WMS-URL: {e}")
