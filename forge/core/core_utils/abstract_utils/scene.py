def exists(node, *args, **kwargs):
    return True


def rename(node_dag, name):
    return name


def safe_delete(node_dag):
    del node_dag


def is_exact_type(node, typename):
    """node.type() == typename"""
    return type(node) == typename


def is_type(node, typename):
    """Return True if node.type() is typename or
    any subclass of typename."""
    return isinstance(node, str)


def get_scene_tree():
    return {}


def list_scene_nodes(object_type='transform', has_shape=False):
    return []

def duplicate(node_dag, parent_only=True, **kwargs):
    return node_dag+'1'