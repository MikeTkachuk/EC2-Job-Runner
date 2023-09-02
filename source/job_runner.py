import time
from pathlib import Path
import os
from typing import Iterable, Union, Tuple
import zipfile

import boto3

from source.compute_instance import InstanceContext
from source.logger import LogListener


class JobRunner:
    def __init__(self,
                 repo_root: Union[str, Path],
                 bucket_name: str,
                 run_prefix: str,
                 instance_id: str,
                 region_name: str,
                 ssh_file_path: Union[Path, str],
                 commands: Iterable[str],
                 ignore_patterns: Tuple[str] = (),
                 loggers: Iterable[LogListener] = None
                 ):
        """

        :param bucket_name:
        :param run_prefix:
        :param instance_id:
        :param region_name:
        :param ssh_file_path:
        :param commands: list of strings. Will be executed in the order provided.
        :param loggers: optional iterable of log listeners. starts every listener on job run.
        """
        self.repo_root = Path(repo_root)
        self.ignore_patterns = ignore_patterns

        self.bucket_name = bucket_name
        self.run_prefix = run_prefix

        self.instance_context = InstanceContext(instance_id, region_name)
        self.ssh_file_path = ssh_file_path
        self.commands = commands
        self.loggers = loggers

    def upload_code(self, repo_root, ignore_patterns=()):
        repo_root = Path(repo_root)

        zip_path = Path(repo_root.name + '.zip')
        with zipfile.ZipFile(zip_path, mode='w') as zip_code:
            for file in repo_root.rglob("*"):
                rel_file = file.relative_to(repo_root)
                if any([rel_file.match(pattern) for pattern in ignore_patterns]):
                    continue
                zip_code.write(file, arcname=rel_file)

        print('JobRunner.upload_code: code upload started')
        # upload code if needed
        name_on_bucket = f"{self.run_prefix}/{zip_path}"
        os.system(f'aws s3 cp {zip_path} s3://{self.bucket_name}/{name_on_bucket} '
                  f'--quiet')
        zip_path.unlink()
        print('JobRunner.upload_code: code upload finished')

    def init_job(self):
        s3_client = boto3.client('s3')
        for logger in self.loggers:
            logger.init(s3_client)
        self.upload_code(self.repo_root, ignore_patterns=self.ignore_patterns)

    def run(self):
        self.init_job()
        with self.instance_context:
            self.instance_context.connect(self.ssh_file_path)
            if self.loggers is not None:
                for logger in self.loggers:
                    logger.start()
            try:
                time.sleep(5)  # prevents unfinished initializations
                for command in self.commands:
                    self.instance_context.exec_command(command)
            finally:
                if self.loggers is not None:
                    for logger in self.loggers:
                        logger.stop()

        return self.instance_context.session_time
