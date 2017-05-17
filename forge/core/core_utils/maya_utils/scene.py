import maya.cmds as mc


def get_scene_tree():
    startup_cams = [mc.listRelatives(c, p=True)[0] for c in mc.ls(cameras=True)
                    if mc.camera(c, q=True, startupCamera=True)]

    top_level_transforms = [node.split('|')[-1] for node in mc.ls(assemblies=True)
                            if node not in startup_cams]

    def recurse_scene_nodes(nodes, tree=None):
        if tree is None:
            tree = {tree_child.split('|')[-1]: dict() for tree_child in nodes}
        elif not tree:
            for tree_child in nodes:
                tree[tree_child.split('|')[-1]] = dict()

        for tree_child in nodes:
            relative_tree = tree[tree_child.split('|')[-1]]
            children = mc.listRelatives(tree_child, fullPath=True, children=True, type='transform')
            if children:
                recurse_scene_nodes(children, relative_tree)

        return tree

    return recurse_scene_nodes(top_level_transforms)


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
