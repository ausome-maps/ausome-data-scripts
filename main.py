#!env/bin/python3

import csv
import json
import os
import sys
import overpass


def _build_query(area):
  return f'''area[name="{area}"] -> .searchArea; node["amenity"="school"](area.searchArea)'''

def _downloader(overpass_query):
  api = overpass.API(timeout=600)
  response = api.get(overpass_query, verbosity='geom')
  return response

def _create_json(data, output="output/test.geojson"):
  with open(output, "w") as output_json:
    json.dump(data, output_json)

def _read_csv(province="data/province.csv"):
  with open(province, "r") as prov_csv:
    provinces = csv.reader(prov_csv)
    next(provinces)
    return provinces

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
      if region == "13": continue # skip NCR since it doesn't use provinces convention
      else: province_list += _transform_to_province_json(file_path, region)
  return province_list

def _build_cities(cities_path):
  """
  for NCR, using the municities dataset
  """
  ncr_list = []
  files = ["municities-province-ph133900000.0.001.json","municities-province-ph137400000.0.001.json", "municities-province-ph137500000.0.001.json", "municities-province-ph137600000.0.001.json"]
  for f in files:
    file_path = os.path.join(cities_path, f)
    ncr_list += _transform_to_province_json(file_path, "NCR")
  return ncr_list

def transform_to_simplified_json(province_path="data/philippines-json-maps/geojson/provinces/lowres", cities_path="data/philippines-json-maps/geojson/municties/lowres/", output_path="data/provinces.json"):
  geo_list = _build_provinces(province_path) + _build_cities(cities_path)
  print("creating provinces and cities index")
  _create_json(geo_list, output_path)

if __name__ == "__main__":
  if sys.argv[1] == "transform-to-simplified-json":
    transform_to_simplified_json()
  else:
    print("module not yet created")
    raise SystemExit(2)
  # if (args_count := len(sys.argv)) > 2:
  #   print(f"One argument expected, got {args_count - 1}")
  #   raise SystemExit(2)
  # elif args_count < 2:
  #   print("You must specify the target directory")
  #   raise SystemExit(2)

  # province = "Manila" # this is only for test
  # os.makedirs("output", exist_ok=True)
  # query = _build_query(province)
  # data = _downloader(query)
  # _create_json(data, f"output/{province}.geojson")
