from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Dict
from typing import List
from typing import Optional

from open_horadric.nodes.root import Root

if TYPE_CHECKING:
    from open_horadric.converters.base.converter import BaseConverter
    from open_horadric.dumpers.base.dumper import BaseDumper
    from open_horadric.parsers.base.parser import BaseParser
    from open_horadric.parsers.base.source import BaseSource


__all__ = ("Pipeline", "PipelineTreeNode")


class Pipeline:
    def __init__(self, parser: BaseParser, pipeline_forest: List[PipelineTreeNode]):
        self.parser: BaseParser = parser
        self.pipeline_forest: List[PipelineTreeNode] = pipeline_forest

    def run(self, sources: List[BaseSource]) -> Dict[str, str]:
        root = self.parser.parse(sources=sources)

        node_root_tree = NodeRootTreeNode()
        node_root_tree.root = root
        for node in self.pipeline_forest:
            node_root_tree[node] = NodeRootTreeNode()
            self.apply_convert(node=node, root=root, node_root_tree=node_root_tree[node])

        output = {}
        for node in self.pipeline_forest:
            self.apply_dump(node=node, node_root_tree=node_root_tree, output=output)

        return output

    def apply_convert(self, node: PipelineTreeNode, root: Root, node_root_tree: NodeRootTreeNode):
        if node.converter is None:
            result_root = root
        else:
            result_root = node.converter.convert(root)

        node_root_tree.root = result_root
        for child in node.children:
            node_root_tree[child] = NodeRootTreeNode()
            self.apply_convert(node=child, root=result_root, node_root_tree=node_root_tree[child])

    def apply_dump(self, node: PipelineTreeNode, node_root_tree: NodeRootTreeNode, output: Dict[str, str]):
        for dumper in node.dumpers:
            output.update(dumper.dump(root=node_root_tree[node].root))

        for child in node.children:
            self.apply_dump(node=child, node_root_tree=node_root_tree[node], output=output)


class PipelineTreeNode:
    def __init__(self, converter: Optional[BaseConverter] = None, dumpers: List[BaseDumper] = None):
        if dumpers is None:
            dumpers = []

        self.converter = converter
        self.dumpers = dumpers
        self.children: List[PipelineTreeNode] = []


class NodeRootTreeNode(dict):
    def __init__(self, **kwargs: Dict[PipelineTreeNode, NodeRootTreeNode]):
        super().__init__(**kwargs)
        self.root: Optional[Root] = None
