import forge
from forge.core.nodes.base.element import AbstractElement


@forge.register_node
class MayaElement(AbstractElement):

    def _layout_guide_cleanup(self):
        raise NotImplementedError

    def _layout_guide_joints(self):
        raise NotImplementedError

    def _layout_guide_connections(self):
        raise NotImplementedError

    def _layout_guide_controls(self):
        raise NotImplementedError
