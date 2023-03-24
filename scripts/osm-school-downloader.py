#!env/bin/python3
import json
import os
import sys
import time
import overpass


def _build_query(area, geo_type="node", overpass_query='"specialized_education" = "special_needs"'):
  return f'''area[name="{area}"] -> .searchArea; {geo_type}[{overpass_query}](area.searchArea)'''

def _downloader(overpass_query):
  """
  triggers the download from the overpass api
  """
  api = overpass.API(timeout=600)
  try: response = api.get(overpass_query, verbosity='geom')
  except: response = {"features": []}
  print(f'fetched {len(response["features"])} schools.')
  return response

def _create_json(data, output="../output/test.geojson"):
  """
  triggers the download from the overpass api
  """
  with open(output, "w") as output_json:
    json.dump(data, output_json)

def _read_json(prov_json):
  with open(prov_json, "r") as provjson:
    prov_data = json.load(provjson)
  return prov_data

def _transform_to_province_json(json_file, region="1"):
  """
  transform a geojson to a simplified province_json
  """
  prov_list = []
  with open(json_file, "r") as jsonfile:
    json_data = json.load(jsonfile)
    for d in json_data["features"]:
      if region == "NCR": province = d["properties"]["ADM3_EN"]
      else: province = d["properties"]["ADM2_EN"]
      prov_list.append({"province": province, "region": d["properties"]["ADM1_EN"]})
  return prov_list

def _build_provinces(province_path):
  """
  general province name extraction
  """
  province_list = []
  for root, dirs, files in os.walk(province_path):
    for f in files:
      file_path = os.path.join(root, f)
      region = f.split("-")[2].split(".")[0].split("ph")[1][0:2]
      if region == "13": province_list += [{"province": "Metro Manila", "region": "National Capital Region"}]
      else: province_list += _transform_to_province_json(file_path, region)
  return province_list

def transform_to_simplified_json(province_path="data/philippines-json-maps/geojson/provinces/lowres", output_path="data/provinces.json"):
  geo_list = _build_provinces(province_path)
  print("creating provinces and cities index")
  _create_json(geo_list, output_path)

def download_nodes(province_path="data/provinces.json", output="output", query_type="base"):
  provinces = _read_json(province_path)
  os.makedirs("output", exist_ok=True)
  for province in provinces:
    output_file = f'{output}/{province["region"]}-{province["province"]}.geojson'
    if query_type == "base": query = _build_query(province["province"], overpass_query='"amenity"="school"' )
    else: query = _build_query(province["province"], overpass_query='"specialized_education" = "special_needs"')
    print(f"running query: ", query)
    data = _downloader(query)
    if len(data["features"]) > 0: _create_json(data, output_file)
    time.sleep(5)


if __name__ == "__main__":
  if sys.argv[1] == "transform-to-simplified-json":
    transform_to_simplified_json()
  elif sys.argv[1] == "download-nodes":
    download_nodes()
  elif sys.argv[1] == "download-specialized-education-nodes":
    download_nodes(query_type="specialized-education")
  else:
    print("module not yet created")
    raise SystemExit(2)

