from pathlib import Path

from source.job_runner import JobRunner
from source.logger import LogListener


commands = [
    "aws cp s3://example_bucket/example_run_prefix ~/example_run_prefix --recursive",
    ""
]

job_runner = JobRunner(
    repo_root=Path(__file__).parents[1],
    bucket_name='example_bucket',
    run_prefix="example_run_prefix",
    instance_id="foo",
    region_name="us-east-1",
    ssh_file_path="path/to/keyfile",
    commands=commands
)