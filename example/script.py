import os
import json

to_log = {"foo": 0, "bar": 1}
with open("metrics.json", "w") as metrics_file:
    json.dump(to_log, metrics_file)
os.system("aws s3 cp metrics.json s3://example_bucket/example_run_prefix/metrics.json")
