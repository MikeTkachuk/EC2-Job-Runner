import os
import json
import argparse
import time


argparser = argparse.ArgumentParser()
argparser.add_argument("--run_prefix", type=str)
argparser.add_argument("--bucket_name", type=str)

args = argparser.parse_args()


to_log = {"foo": 0, "bar": time.time()}
with open("metrics.json", "w") as metrics_file:
    json.dump(to_log, metrics_file)
os.system(f"aws s3 cp metrics.json s3://{args.bucket_name}/{args.run_prefix}/metrics.json")
