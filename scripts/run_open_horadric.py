import logging
import os
import subprocess
import sys

import yaml

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

logger = logging.getLogger("open_horadric.cmd")
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


def create_cmd(protoc_path: str, proto_dir: str, output_dir):
    # FIXME: relative paths
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
        "--plugin=protoc-gen-wrapper={}".format(os.path.abspath("open_horadric/plugin.py")),
        "--wrapper_out={}".format(wrapper_output),
    ] + proto_files

    return parts


def get_config() -> dict:
    with open(os.environ.get("CONFIG", "config.yaml")) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def main():
    config = get_config()
    protoc_path = config.get("protoc_path", "protoc")
    proto_dir = os.path.abspath(config.get("proto_dir", "proto"))
    protoc_version = config.get("protoc_version")
    output_dir = os.path.abspath(config.get("output_dir", "generated"))

    exists_protoc_version = subprocess.check_output((protoc_path, "--version")).strip().split()[-1].decode()
    logger.info("%-12s v%s (%s)", "protoc", exists_protoc_version, protoc_path)

    if protoc_version and exists_protoc_version != protoc_version:
        logger.error("libprotoc %s required", protoc_version)
        sys.exit(1)

    cmd = create_cmd(protoc_path=protoc_path, proto_dir=proto_dir, output_dir=output_dir)
    logger.info("Run compile command: %s", " ".join(cmd))
    subprocess.check_call(cmd, stdout=sys.stdout, stderr=sys.stderr)


if __name__ == "__main__":
    main()
