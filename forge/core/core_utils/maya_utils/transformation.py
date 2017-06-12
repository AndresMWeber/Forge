import maya.cmds as mc


def zero_local_space(transform_dag, **kwargs):
    return mc.makeIdentity(transform_dag, **kwargs)
