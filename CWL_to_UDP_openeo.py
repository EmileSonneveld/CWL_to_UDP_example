from pathlib import Path

import openeo

url = "https://openeo.dataspace.copernicus.eu"
connection = openeo.connect(url).authenticate_oidc()

# datacube = connection.load_collection(
#     "SENTINEL2_L2A",
#     spatial_extent={"east": 5.08, "north": 51.22, "south": 51.215, "west": 5.07},
#     temporal_extent=["2023-06-01", "2023-06-06"],
#     bands=["B04", "B03", "B02"],
# )
# output_path = Path("tmp_load_collection_output")

# This simple CWL wilt output unscaled sentinel2 STAC data, quite like the load_collection equivalent:
datacube = connection.datacube_from_process(
    "run_udf",
    data=None,
    udf="https://raw.githubusercontent.com/Open-EO/openeo-geotrellis-kubernetes/master/openeo-geopyspark-k8s-custom-processes/src/openeo_geopyspark_k8s_custom_processes/cwl/dummy_stac.cwl",
    runtime="EOAP-CWL",
    context={},
)
output_path = Path("tmp_run_udf_output")

datacube = connection.datacube_from_process(
    "linear_scale_UDP",
    namespace="https://raw.githubusercontent.com/EmileSonneveld/CWL_to_UDP_example/refs/heads/main/linear_scale_UDP.json",
    input_datacube=datacube,
)

output_path.mkdir(exist_ok=True)
job = datacube.create_job(title=__file__)
job.start_and_wait()
job.get_results().download_files(output_path)
