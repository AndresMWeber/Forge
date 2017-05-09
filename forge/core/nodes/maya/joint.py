import maya.cmds as mc
from forge.rig_lib.core.nodes.base.joint import AbstractJoint

import forge
from forge.core.nodes.maya.transform import MayaTransform


@forge.register_node
class MayaJoint(MayaTransform, AbstractJoint):
    """
         Wraps a dag_path with generic functions to manipulate a maya joint node
    """
    def __init__(self, node_dag='', *args, **kwargs):
        super(MayaJoint, self).__init__(node_dag=node_dag, *args, **kwargs)

    def color(self, color_index):
        mc.color(self.node, ud=color_index)
