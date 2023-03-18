# PH School OSM Downloader
The following repository will download PH schools from OSM. This will produce a GeoJSON file which is named after the province where the school is located.


## Requirements
- Overpass

## Setup
1. Setup a virtual environment: `python3 -m venv env`
2. Install python dependencies: `pip install -r requirements.txt`

## Datasets
- [Province List](https://github.com/faeldon/philippines-json-maps)

## Usage
- **transform-to-simplified-json:** creates a provinces JSON which contains the provinces and NCR cities into one. 
    ```
    ./main.py transform-to-simplified-json
    ```

