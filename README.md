# Ausome Data Scripts
This repository contains the data scripts of ausome maps to work with OSM datasets.


## Requirements
- Overpass
- Python 3.8+

## Setup
1. Setup a virtual environment: `python3 -m venv env`
2. Install python dependencies: `pip install -r requirements.txt`

## Datasets
- [Province List](https://github.com/faeldon/philippines-json-maps)

## Scripts
This folder contains some of the scripts used by ausome maps to work with OSM data.

### OSM School Downloader
- **transform-to-simplified-json:** creates a provinces JSON which contains the provinces and NCR cities into one. _There is already a `province.json` which the download-nodes use._
    ```
    ./scripts/osm-school-downloader.py transform-to-simplified-json
    ```
- **download-nodes:** this uses Overpass Turbo API to download the `amenity=school` from OSM. This will produce an output folder containing the GeoJSON files of the downloaded nodes..
   ```
   ./scripts/osm-school-downloader.py download-nodes
   ```
- **download-specialized-education-nodes:** This uses Overpass Turbo API to download the `specialized_education=special_needs` from OSM. This will produce an output folder containing the GeoJSON files of the downloaded nodes.
   ```
   ./scripts/osm-schoold-downloader.py download-specialized-education-nodes
   ```

## How to Contribute?
- Add your script under the `scripts` directory.
- Update the `requirements.txt` for any new python dependency.
- Update the `README.md` to add the usage of your code.
