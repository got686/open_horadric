from __future__ import annotations

from open_horadric.parsers.proto3.parser import Proto3Parser
from open_horadric.pipelines.base_pipelines.open_api.main_tree import open_api_main_tree
from open_horadric.pipelines.pipeline import Pipeline

open_api_pipeline = Pipeline(parser=Proto3Parser(), pipeline_forest=[open_api_main_tree])
