import requests
import xmltodict
import os
import json
import re

def fetch_catalog_save_response(
        save_dir="tmp"
        ):
    """
    Call hard coded Catalog API and loop over language version and save it as separate json files
    Returns:
    dict: {
        "saved_files": [...],
        "errors": [...]
    }
    """
    
    # Define storage directory
    os.makedirs(save_dir, exist_ok=True)


    lang = ["de", "en", "fr", "it"]
    catalog_array = []
    errors = []

    for l in lang:
        try:
            url = f"https://api3.geo.admin.ch/rest/services/geol/CatalogServer?lang={l}"
            print(url)

            # Filter Characters after "https://" and "." in service-URL 
            match = re.search(r"^https://([^\.]+)\.", url)
            if match:
                typ = match.group(1)  # saves "wms" or "wmts"
                print(typ)
            else:
                typ = f"unkown_{l}"

            catalog_path = os.path.join(save_dir, f'{typ}_{l}.json')
            catalog_array.append(catalog_path)
            
            print(catalog_path)

            # API abfragen
            response = requests.get(url)
            response.raise_for_status

            data = response.json()

            # Auf Dateisystem speichern
            with open(f"{catalog_path}", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Data successfully saved in {typ}_{l}.json gespeichert.")

    
        except requests.exceptions.RequestException as e:
            errors.append(f"Request error for lang={l}: {e}")
        except json.JSONDecodeError as e:
            errors.append(f"JSON decode error for lang={l}: {e}")
        except Exception as e:
            errors.append(f"Unexpected error for lang={l}: {e}")

    return {"saved_files": catalog_array, "errors": errors}


def fetch_wmts_wms_save_response(
    save_dir = "tmp"
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

            print(xml_path)

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
        