#!/usr/bin/env python

import logging
import os
import subprocess
import sys

from open_horadric.config.config import Config

logger = logging.getLogger("open_horadric.cmd")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

CURRENT_DIR = os.path.dirname(__file__)


def create_cmd(protoc_path: str, proto_dir: str, output_dir):
    proto_files = []
    import os

    for root, dirs, files in os.walk(proto_dir):
        for name in files:
            if name.endswith(".proto"):
                proto_files.append(os.path.join(root, name))
            else:
                raise ValueError("Invalid file extension in file {}".format(os.path.join(root, name)))

    wrapper_output = os.path.join(output_dir, "output")
    pb2_output = os.path.join(output_dir, "pb2")
    os.makedirs(wrapper_output, exist_ok=True)
    os.makedirs(pb2_output, exist_ok=True)

    parts = [
        protoc_path,
        "--python_out={}".format(pb2_output),
        "--proto_path={}".format(proto_dir),
        "--plugin=protoc-gen-wrapper={}".format(os.path.join(CURRENT_DIR, "_open_horadric_plugin.py")),
        "--wrapper_out={}".format(wrapper_output),
    ] + proto_files

    return parts


def main():
    config = Config()
    proto_dir = os.path.abspath(config.proto_dir)
    output_dir = os.path.abspath(config.output_dir)

    exists_protoc_version = subprocess.check_output((config.protoc_path, "--version")).strip().split()[-1].decode()
    logger.info("%-12s v%s (%s)", "protoc", exists_protoc_version, config.protoc_path)

    if config.protoc_version and exists_protoc_version != config.protoc_version:
        logger.warning("libprotoc %s required", config.protoc_version)

    cmd = create_cmd(protoc_path=config.protoc_path, proto_dir=proto_dir, output_dir=output_dir)
    logger.info("Run compile command: %s", " ".join(cmd))
    subprocess.check_call(cmd, stdout=sys.stdout, stderr=sys.stderr)

    for command in config.run_after:
        logger.info("Run command: %s", command)
        subprocess.check_call(["bash", "-c", command], stdout=sys.stdout, stderr=sys.stderr)
        logger.info("End running command: %s", command)


if __name__ == "__main__":
    main()
