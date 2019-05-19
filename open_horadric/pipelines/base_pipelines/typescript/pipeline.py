from __future__ import annotations

from open_horadric.parsers.proto3.parser import Proto3Parser
from open_horadric.pipelines.base_pipelines.typescript.main_tree import typescript_main_tree
from open_horadric.pipelines.pipeline import Pipeline

typescript_pipeline = Pipeline(parser=Proto3Parser(), pipeline_forest=[typescript_main_tree])
