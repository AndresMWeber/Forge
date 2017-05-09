import maya.cmds as mc

def connect_attr(attr_source, attr_destination, **kwargs):
    mc.connectAttr(attr_source, attr_destination, **kwargs)

def set_attr (node_attr_dag, *args, **kwargs):
    mc.setAttr(node_attr_dag, *args, **kwargs)

def add_attr(node, **kwargs):
    mc.addAttr(node, **kwargs)
