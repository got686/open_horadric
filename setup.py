from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="open_horadric",
    version="0.0.2dev",
    python_requires=">=3.7",
    packages=find_namespace_packages(include=("open_horadric*",)),
    install_requires=["protobuf>=3.9.1", "grpcio>=1.23.0", "jinja2>=2.10.1", "pyyaml>=5.1.2"],
    dependency_links=["git+https://github.com/got686/open_horadric_lib@572a8d946a8e6f54c112f9c29aebb9dab8227aef"],
    url="https://github.com/got686/open_horadric",
    license="MIT",
    author="got686",
    author_email="got686@yandex.ru",
    description="Code gen from protobuf to some other things",
    scripts=["scripts/run_open_horadric.py", "scripts/_open_horadric_plugin.py"],
    include_package_data=True,
)
