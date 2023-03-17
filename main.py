import json
import os
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

if __name__ == "__main__":
  province = "Manila" # this is only for test
  os.makedirs("output", exist_ok=True)
  query = _build_query(province)
  data = _downloader(query)
  _create_json(data, f"output/{province}.geojson")
