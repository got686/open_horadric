from __future__ import annotations

from open_horadric.parsers.proto3.parser import Proto3Parser
from open_horadric.pipelines.base_pipelines.py3.main_tree import py3_main_tree
from open_horadric.pipelines.pipeline import Pipeline

py3_pipeline = Pipeline(parser=Proto3Parser(), pipeline_forest=[py3_main_tree])
