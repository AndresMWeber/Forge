import maya.cmds as mc


def list_hierarchy(topJoint, withEndJoints=True):
    """ list joint hierarchy starting with top joint
    :param topJoint: str, joint to get listed with its joint hierarchy
    :param withEndJoints: bool, list hierarchy including end joints
    :return: list( str ), listed joints starting with top joint
                        (if empty, returns full list of children joints)
    """
    listedJoints = mc.listRelatives(topJoint, type='joint', ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()

    completeJoints = listedJoints[:]

    if not withEndJoints:
        completeJoints = [j for j in listedJoints if mc.listRelatives(j, c=1, type='joint')]

    return completeJoints

