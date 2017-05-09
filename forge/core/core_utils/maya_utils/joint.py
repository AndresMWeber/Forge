import nomenclate
import pymel.core as pm

import forge
import transformation

nom = nomenclate.Nom()


def listHierarchy(topJoint, withEndJoints=True):
    """ list joint hierarchy starting with top joint
    :param topJoint: str, joint to get listed with its joint hierarchy
    :param withEndJoints: bool, list hierarchy including end joints
    :return: list( str ), listed joints starting with top joint
                        (if empty, returns full list of children joints)
    """
    listedJoints = pm.listRelatives(topJoint, type='joint', ad=True)
    listedJoints.append(topJoint)
    listedJoints.reverse()

    completeJoints = listedJoints[:]

    if not withEndJoints:
        completeJoints = [j for j in listedJoints if pm.listRelatives(j, c=1, type='joint')]

    return completeJoints


def get_chain(startJoint, endJoint=False):
    '''Takes two joints as inputs and then returns the children joints in between the two inputs.
    Args:
        startJoint (pm.PyNode): the starting joint of the chain
        endJoint (pm.PyNode): the ending joint of the chain (if empty, returns full list of children joints)
    Returns: (List [pm.PyNode)) - the list of joints in the chain
    '''
    results = [startJoint]
    children = startJoint.listRelatives(c=True, type="joint")
    if len(children) > 0:
        for child in children:
            if child != endJoint:
                results.extend(rig_getJointChain(child, endJoint))
            elif endJoint != False:
                results.append(child)
    return results


def make_joints_along_curve(curve, num_joints=0, rebuild=False, parent=None, **kwargs):
    """ Create joints along a curve in the same direction as the curve
    :param curve: pm.PyNode, the curve transform to be used
    :param name: 
    :param num_joints: int, the number of joints to be created, if 0 will use CVs
    :param rebuild: bool, whether we rebuild and normalize the curve or not
    :param parent: pm.nt.Transform, final parent of the joints
    :return: list(pm.nt.Joint): created joints
    :usage:
        rig_makeJointsAlongCurve("petalA", pm.ls(sl=True)[0], 15)
        rig_makeJointsAlongCurve("seatbeltDrive", pm.ls(sl=True)[0], 160)
    """
    nom.merge_dict({'name': 'untitled', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    poci = None

    # Creating a curve between them
    curve = pm.duplicate(curve)[0]

    if rebuild:
        pm.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=1, kcp=0, kep=1, kt=0,
                        s=num_joints, d=1, tol=0.01)

    # Detecting if we're doing cv based or not
    if not num_joints:
        cvs = True
        num_joints = curve.getShape().numCVs() - 1
    else:
        cvs = False
        poci = pm.createNode('pointOnCurveInfo')
        curve.getShape().worldSpace[0].connect(poci.inputCurve)
        poci.turnOnPercentage.set(1)

    # Evenly spacing joints according to the curve
    joints = []
    names = nom.get_chain(num_joints)

    # Clear the selection since the stupid joint command sucks at parenting
    pm.select(cl=True)
    for joint_index, name in enumerate(names):
        if cvs:
            jnt_pos = pm.pointPosition(curve.getShape().cv[joint_index], w=1)
        else:
            poci.parameter.set(float(joint_index) / float(num_joints))
            jnt_pos = poci.position.get()

        joints.append(pm.joint(n=name, p=jnt_pos))

    # Set the rotation order
    for joint in joints[:-1]:
        joint.secondaryAxisOrient('yup', oj='xyz')

    # if parent is set, do it.
    if parent:
        pm.setParent(joints[0], parent)

    # Cleanup
    pm.delete(curve)
    if cvs:
        pm.delete(poci)

    return joints


def build_from_points(transforms, chain=False, parent=None, offset=False, freeze=True, **kwargs):
    """ Create joints based on given 3D spatial positions/rotations e.g. [[[10,5.3,1.4],[0,90,0]],...,nPos]
    Args:
        transforms [[float,float,float]] or [pm.nt.Transform]: 
            list of transforms xyz coordinate + euler rotation based or pm.nt.Transform
        prefix (str): base name for the chain
        chain (bool): whether or not to make a chain, or isolated joints
        offset (bool): whether or not to build in offset groups for the joints
        parent (pm.nt.Transform): final parent of the joints, empty if kept at root level
    Returns:
        [pm.nt.Joint]: list of joints
    Usage:
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=True)
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=False)
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=False, parent='null1')
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=True, parent='null1')
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', chain=True, offset=True, parent='null1')
        build_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', chain=True, offset=False, parent='null1')
    """
    nom.merge_dict({'name': 'chain', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    # Evenly spacing joints according to the curve
    joints = []

    # inital setup (setting var just in case it's not overridden)
    names = nom.get_chain(len(transforms))

    for jnt_pos, name in zip(transforms, names):
        # Just in case we're dealing with pm.nt.Transform objects
        if isinstance(jnt_pos, pm.nt.Transform):
            buffer = pm.spaceLocator()
            pm.delete(pm.parentConstraint(jnt_pos, buffer))
            jnt_pos = [buffer.translate.get(), buffer.rotate.get()]
            pm.delete(buffer)

        t, r = jnt_pos
        joint = pm.createNode('joint', n=name)
        joint.translate.set(t)
        joint.rotate.set(r)
        joints.append(joint)

    # Build offset groups
    if offset:
        nom.decorator = 'Offset'
        nom.type = 'group'
        offset_names = nom.get_chain(len(transforms))

        for offset_name, joint in zip(offset_names, joints):
            offset = forge.registry.transform.create(offset_name, joint)
            joint.parent(offset)
            # Now we have to set the joint up with these orientations from the offset group
            pm.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0, pn=1)
            joint.jointOrient.set([0, 0, 0])

    # Do chain parenting at the end to preserve rotations
    if chain:
        joint_parents = [joint for joint in joints]
        joint_parents.reverse()
        for index, joint in enumerate(joint_parents):
            try:
                joint = joint.getParent() or joint
                pm.parent(joint, joint_parents[index + 1])
            except IndexError:
                pass

    # Freeze transforms in case that we didn't make offset groups
    if freeze and not chain:
        for joint in joints:
            pm.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # if overall parent is set, do it for all cases
    if parent:
        if chain:
            to_parent = joints[0].getParent() or joints[0]
        elif offset and not chain:
            # Just in case offsets need to be parented instead
            to_parent = [joint.getParent() for joint in joints]
        else:
            to_parent = joints

        pm.parent(to_parent, parent)

    return joints


def build_between_points(start_xform, end_xform, n_joints, freeze=True, chain=True, parent=None, offset=False,
                         **kwargs):
    """ Create joints based on given 3D spatial positions/rotations e.g. [[[10,5.3,1.4],[0,90,0]],...,nPos]
    Args:
        start_xform [pm.nt.Transform]: starting position
        end_xform [pm.nt.Transform]: ending position
        name (str): base name for the chain
        chain (bool): whether or not to make a chain, or isolated joints
        offset (bool): whether or not to build in offset groups for the joints
        parent (pm.nt.Transform): final parent of the joints, empty if kept at root level
    Returns:
        [pm.nt.Joint]: list of joints
    Usage:
        Joint.build_between_points(pm.ls(sl=True)[0], pm.ls(sl=True)[1], 5, chain=True, offset=True, freeze=True)
    """
    nom.merge_dict({'name': 'chain', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    xform_interps = transformation.spatial_interpolate(pm.xform(start_xform, q=True, t=True, ws=True),
                                                       pm.xform(end_xform, q=True, t=True, ws=True),
                                                       n_joints)

    rotation_interps = transformation.spatial_interpolate(pm.xform(start_xform, q=True, ro=True, ws=True),
                                                          pm.xform(end_xform, q=True, ro=True, ws=True),
                                                          n_joints)

    positions = [[xform_interp, rotation_interp] for xform_interp, rotation_interp in
                 zip(xform_interps, rotation_interps)]

    return build_from_points(positions, chain=chain, parent=parent, offset=offset, freeze=freeze, **kwargs)


def insert_between_joints(start_joint, end_joint, joint_num, bone_translate_axis='tx', **kwargs):
    """
    Args:
        start_joint (pm.nt.Transform): start position
        end_joint (pm.nt.Transform): start position
        joint_num (int): number of joints
        bone_translate_axis (str): what axis to follow for the joints, options: tx, ty, tz
        name (dict): nomenclate dictionary
    Returns [pm.nt.Joint]: list of joints
    Usage:
        Joint.insert_between_joints(pm.ls(sl=True)[0], pm.ls(sl=True)[1], 5)
        Joint.insert_between_joints(pm.ls(sl=True)[0], pm.ls(sl=True)[1], 5, bone_translate_axis='tz')
    """
    nom.merge_dict({'name': 'twist', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    names = nom.get_chain(joint_num)

    last_joint, joints = None, []
    bone_length = end_joint.attr(bone_translate_axis).get()

    for name in names:
        joint = pm.createNode('joint', name=name)
        pm.parent(joint, start_joint, relative=True)
        joint.attr(bone_translate_axis).set(bone_length / (joint_num + 1))
        if last_joint:
            pm.parent(joint, last_joint, relative=True)
        if name == names[-1]:
            pm.parent(end_joint, joint)
        last_joint = joint
        joints.append(joint)

    return joints
