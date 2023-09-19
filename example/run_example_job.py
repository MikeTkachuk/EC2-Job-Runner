from pathlib import Path

from source.job_runner import JobRunner
from source.logger import LogListener

run_prefix = "example_run_prefix"
bucket_name = "example_bucket"
repo_root = Path(__file__).parents[1]


def log_func(x, step=None, name=None):
    print(f"{x} step={step} name={name}")


logger = LogListener(log_func, f"{run_prefix}/metrics.json", bucket_name=bucket_name, name="example_listener")
commands = [  # executes directly at an instance's terminal
    f"cd ~/{run_prefix}/{repo_root.name}",
    f"python example/script.py --bucket_name {bucket_name} --run_prefix {run_prefix}",  # plain script call
    f"sh run.sh {bucket_name} {run_prefix}"  # same script call + dir cleanup (see the script itself)
]

job_runner = JobRunner(
    repo_root=repo_root,
    bucket_name=bucket_name,
    run_prefix=run_prefix,
    instance_id="foo",
    region_name="us-east-1",
    ssh_file_path="path/to/keyfile",
    commands=commands,
    loggers=[logger]
)

# if auto-setup is turned on, the code is automatically downloaded
# and unzipped in ~/example_run_prefix/
job_runner.run(auto_setup=True)

# if auto-setup is off, you can perform an equivalent setup by running:
commands = [
    f'aws s3 cp s3://{bucket_name}/{run_prefix} ~/{run_prefix} --recursive',
    f"unzip -q ~/{run_prefix}/{repo_root.name}.zip -d ~/{run_prefix}/{repo_root.name}",
    f"cd ~/{run_prefix}/{repo_root.name}",
    "sh run.sh"
]

job_runner.commands = commands
job_runner.run(auto_setup=False)
