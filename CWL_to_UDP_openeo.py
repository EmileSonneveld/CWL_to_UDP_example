import openeo

url = "https://openeo.dataspace.copernicus.eu"
connection = openeo.connect(url).authenticate_oidc()

datacube = connection.load_collection(
    "SENTINEL2_L2A",
    spatial_extent={"east": 5.08, "north": 51.22, "south": 51.215, "west": 5.07},
    temporal_extent=["2025-06-01", "2025-06-06"],
    bands=["B04", "B03", "B02"],
)
datacube = connection.datacube_from_process(
    "linear_scale_UDP",
    namespace="https://raw.githubusercontent.com/EmileSonneveld/CWL_to_UDP_example/refs/heads/main/linear_scale_UDP.json",
    input_datacube=datacube,
)

job = datacube.create_job()
job.start_and_wait()
results = job.get_results()
