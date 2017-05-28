import maya.cmds as mc


def connect_attr(attr_source, attr_destination, **kwargs):
    return mc.connectAttr(attr_source, attr_destination, **kwargs)


def set_attr(node_attr_dag, *args, **kwargs):
    return mc.setAttr(node_attr_dag, *args, **kwargs)


def get_attr(node_attr_dag, *args, **kwargs):
    return mc.getAttr(node_attr_dag, *args, **kwargs)


def add_attr(node, **kwargs):
    return mc.addAttr(node, **kwargs)
