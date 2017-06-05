import maya.cmds as mc
from forge.core.nodes.base.joint import AbstractJoint

import forge
from forge.core.nodes.maya.transform import MayaTransform


@forge.register_node
class MayaJoint(MayaTransform, AbstractJoint):
    """
         Wraps a dag_path with generic functions to manipulate a maya joint node
    """

    def __init__(self, node_dag='', *args, **kwargs):
        super(MayaJoint, self).__init__(node_dag=node_dag, *args, **kwargs)

    @staticmethod
    def create_engine_instance(node_type='group', *args, **kwargs):
        return mc.joint()

    def color(self, color_index):
        mc.color(self.node, ud=color_index)
