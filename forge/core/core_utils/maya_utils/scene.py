import maya.cmds as mc


def list_scene_nodes(object_type='transform', has_shape=False):
    return [transform for transform in mc.ls(type=object_type) if not mc.listRelatives(transform, s=has_shape, c=True)]


def exists(node, *args, **kwargs):
    return mc.objExists(node, *args, **kwargs)


def safe_delete(node_or_nodes):
    if isinstance(node_or_nodes, list):
        for node in node_or_nodes:
            try:
                mc.delete(node)
            except ValueError:
                pass
    else:
        try:
            mc.delete(node_or_nodes)
        except ValueError:
            pass


def rename(node_dag, name, **kwargs):
    mc.rename(node_dag, name, **kwargs)
    return node_dag


def duplicate(node_dag, parent_only=True, **kwargs):
    duplicate_node = mc.duplicate(node_dag, parentOnly=parent_only, **kwargs)[0]
    return duplicate_node
