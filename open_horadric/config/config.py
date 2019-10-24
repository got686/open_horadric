from __future__ import annotations

import os
from typing import Any
from typing import Dict
from typing import List

import yaml
from open_horadric_lib.base.singleton import SingletonMeta

CURRENT_DIR = os.path.dirname(__file__)


class Config(metaclass=SingletonMeta):
    def __init__(self):
        default_config_path = os.path.join(CURRENT_DIR, "default.yaml")
        with open(default_config_path) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            if config is None:
                raise ValueError("Empty config, there is must be at least `project_name`")

        config_path = os.environ.get("CONFIG", "open_horadric_config.yaml")
        with open(config_path) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        config.update(data)

        self.protoc_path: str = config["protoc_path"]
        self.protoc_version: str = config["protoc_version"]
        self.proto_dir: str = config["proto_dir"]
        self.output_dir: str = config["output_dir"]
        self.project_name: str = config["project_name"]
        self.pipelines: Dict[str, Dict[str, Any]] = config["pipelines"]
        self.debug: bool = config["debug"]
        self.version: str = config["version"]
        self.license: str = config["license"]
        self.run_after: List[str] = config["run_after"]
