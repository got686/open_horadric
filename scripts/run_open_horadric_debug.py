import sys

from google.protobuf.compiler import plugin_pb2

from scripts._open_horadric_plugin import generate_response


def main():
    with open("debug_data_dump", "rb") as f:
        data = f.read()

    plugin_request = plugin_pb2.CodeGeneratorRequest()
    plugin_request.ParseFromString(data)
    plugin_response = generate_response(plugin_request)
    output = plugin_response.SerializeToString()

    sys.stdout.buffer.write(output)


if __name__ == "__main__":
    main()
