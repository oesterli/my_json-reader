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
