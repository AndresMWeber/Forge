def exists(node, *args, **kwargs):
    return True


def rename(node_dag, name):
    return name


def safe_delete(node_dag):
    del node_dag
