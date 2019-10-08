from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="open_horadric",
    version="0.0.2dev",
    python_requires=">=3.7",
    packages=find_namespace_packages(include=("open_horadric*",)),
    install_requires=["protobuf>=3.10.1", "grpcio>=1.24.1", "jinja2>=2.10.3", "pyyaml>=5.1.2"],
    dependency_links=["git+https://github.com/got686/open_horadric_lib@d4add9ea95f0c5af38787bef3809fcb9130dcede"],
    url="https://github.com/got686/open_horadric",
    license="MIT",
    author="got686",
    author_email="got686@yandex.ru",
    description="Code gen from protobuf to some other things",
    scripts=["scripts/run_open_horadric.py", "scripts/_open_horadric_plugin.py"],
    include_package_data=True,
)
