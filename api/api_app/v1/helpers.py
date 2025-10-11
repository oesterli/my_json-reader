import requests
import xmltodict
import os
import json
import re

def fetch_service_save_xml_json(
    save_dir="tmp"
):
    """
    Call a hard coded WMS- or WMTS-URL and save response as XML and convert ans save it as JSON
    """

    #  WMS- and WMTS-URL (hard coded)
    wms_url = "https://wms.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities"
    wmts_url = "https://wmts.geo.admin.ch/EPSG/2056/1.0.0/WMTSCapabilities.xml"

    urls = [wms_url, wmts_url]

    # Define storage directory
    os.makedirs(save_dir, exist_ok=True)

    try:
        for url in urls:
            print(url)

            # Filter Characters after "https://" and "." in service-URL 
            match = re.search(r"^https://([^\.]+)\.", url)
            if match:
                typ = match.group(1)  # saves "wms" or "wmts"
                print(typ)
        
            xml_path = os.path.join(save_dir, f'{typ}.xml')
            json_path = os.path.join(save_dir,  f'{typ}.json')

            # Request WMS-Server
            response = requests.get(url, timeout=20)
            response.raise_for_status()

            # Save response as XML 
            with open(xml_path, "w", encoding="utf-8") as f:
                f.write(response.text)

            # Convert XML in Python-Dict
            data_dict = xmltodict.parse(response.text)

            # Save speichern
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data_dict, f, indent=2)    

        return xml_path, json_path, data_dict

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error when calling WMS- or WMTS-URL: {e}")



def get_json():
    """
    Call hard coded Catalog API and loop over language version and save it as separate json files
    """
    save_dir="tmp"
    
    # Define storage directory
    os.makedirs(save_dir, exist_ok=True)


    lang = ["de", "en", "fr", "it"]
    for l in lang:
        url = f"https://api3.geo.admin.ch/rest/services/geol/CatalogServer?lang={l}"
        print(url)

        # Filter Characters after "https://" and "." in service-URL 
        match = re.search(r"^https://([^\.]+)\.", url)
        if match:
            typ = match.group(1)  # saves "wms" or "wmts"
            print(typ)

        catalog_path = os.path.join(save_dir, f'{typ}.json')

        # API abfragen
        response = requests.get(url)

        # Prüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            # JSON-Daten als Python-Objekt
            data = response.json()

            # Variable: Daten sind jetzt in 'data'
            # print("JSON-Daten:", data)
            # print(json.dumps(data, indent=4, ensure_ascii=False))       

            # JSON(data)

            # Auf Dateisystem speichern
            with open(f"{catalog_path}_{l}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Data successfully saved in daten_{l}.json gespeichert.")
        else:
            print(f"Error {response.status_code}: {response.text}")
