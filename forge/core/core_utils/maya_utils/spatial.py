import math

"""
Operates on position data or Maya engine objects to return position arrays.
"""


def spatial_interpolate(start, end, samples):
    """ Interpolate self.start_valueetween two points with a given number of samples
        Usage:
            spatial_interpolate([0,0,0],[0,-10,0], 5)
            spatial_interpolate([24.28, 0.0, 10.72], [26.87, 0.0, -6.72], 5)

    :param start: list(float, float, float), 3d point
    :param end: list(float, float, float), 3d point
    :param samples: int, number of output points including start and end
    :returns: list(list(float, float, float)): list of 3d points
    """
    spx, spy, spz = [abs(x - y) / float(samples - 1) for x, y in zip(start, end)]
    dirX, dirY, dirZ = [-1 if sp > ep else 1 for sp, ep in zip(start, end)]
    mid_points = [[(start[0] + index * spx * dirX),
                   (start[1] + index * spy * dirY),
                   (start[2] + index * spz * dirZ)] for index in range(1, samples - 1)]
    mid_points.insert(0, [float(i) for i in start])
    mid_points.append([float(i) for i in end])
    return mid_points


class Easer(object):
    """ Based on time, starting value, step value and duration returns the specified easing function's result
    
    """

    def __init__(self, time, start_value, step_value, duration):
        """

        :param time: float, the current time we want to query
        :param start_value: float, starting value for the interpolation
        :param step_value: float, the spacing of the steps
        :param duration: float, the duration we are looking to cover
        """
        self.time = time
        self.start_value = start_value
        self.step_value = step_value
        self.duration = duration

    def linear_interpolate(self):
        """ simple linear tweening - no easing, no acceleration

        """
        return self.step_value * self.time / self.duration + self.start_value

    def ease_in_quad(self):
        """ quadratic easing in - accelerating from zero velocity

        """
        self.time /= self.duration
        return self.step_value * self.time * self.time + self.start_value

    def ease_out_quad(self):
        """ quadratic easing out - decelerating to zero velocity

        """
        self.time /= self.duration
        return -self.step_value * self.time * (self.time - 2) + self.start_value

    def ease_in_out_quad(self):
        """ quadratic easing in/out - acceleration until halfway, then deceleration

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return self.step_value / 2 * self.time * self.time + self.start_value
        self.time -= 1
        return -self.step_value / 2 * (self.time * (self.time - 2) - 1) + self.start_value

    def ease_in_cubic(self):
        """ cubic easing in - accelerating from zero velocity

        """
        self.time /= self.duration
        return self.step_value * self.time * self.time * self.time + self.start_value

    def ease_out_cubic(self):
        """ easing out - decelerating to zero velocity

        """
        self.time /= self.duration
        self.time -= 1
        return self.step_value * (self.time * self.time * self.time + 1) + self.start_value

    def ease_in_out_cubic(self):
        """ cubic easing in/out - acceleration until halfway, then deceleration

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return self.step_value / 2 * self.time * self.time * self.time + self.start_value
        self.time -= 2
        return self.step_value / 2 * (self.time * self.time * self.time + 2) + self.start_value

    def ease_in_quartic(self):
        """ quartic easing in - accelerating from zero velocity

        """
        self.time /= self.duration
        return self.step_value * self.time * self.time * self.time * self.time + self.start_value

    def ease_out_quart(self):
        """ quartic easing out - decelerating to zero velocity

        """
        self.time /= self.duration
        self.time -= 1
        return -self.step_value * (self.time * self.time * self.time * self.time - 1) + self.start_value

    def ease_in_out_quartic(self):
        """ quartic easing in/out - acceleration until halfway, then deceleration

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return self.step_value / 2 * self.time * self.time * self.time * self.time + self.start_value
        self.time -= 2
        return -self.step_value / 2 * (self.time * self.time * self.time * self.time - 2) + self.start_value

    def ease_in_quintic(self):
        """ quintic easing in - accelerating from zero velocity

        """
        self.time /= self.duration
        return self.step_value * self.time * self.time * self.time * self.time * self.time + self.start_value

    def ease_out_quintic(self):
        """ quintic easing out - decelerating to zero velocity

        """
        self.time /= self.duration
        self.time -= 1
        return self.step_value * (self.time * self.time * self.time * self.time * self.time + 1) + self.start_value

    def ease_in_out_quint(self):
        """ quintic easing in/out - acceleration until halfway, then deceleration

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return self.step_value / 2 * self.time * self.time * self.time * self.time * self.time + self.start_value
        self.time -= 2
        return self.step_value / 2 * (self.time * self.time * self.time * self.time * self.time + 2) + self.start_value

    def ease_in_sine(self):
        """ sinusoidal easing in - accelerating from zero velocity

        """
        return -self.step_value * math.cos(
            self.time / self.duration * (math.pi / 2)) + self.step_value + self.start_value

    def ease_out_sine(self):
        """ sinusoidal easing out - decelerating to zero velocity

        """
        return self.step_value * math.sin(self.time / self.duration * (math.pi / 2)) + self.start_value

    def ease_in_out_sine(self):
        """ sinusoidal easing in/out - accelerating until halfway, then decelerating

        """
        return -self.step_value / 2 * (math.cos(math.pi * self.time / self.duration) - 1) + self.start_value

    def ease_in_expo(self):
        """ exponential easing in - accelerating from zero velocity

        """
        return self.step_value * math.pow(2, 10 * (self.time / self.duration - 1)) + self.start_value

    def ease_out_expo(self):
        """ exponential easing out - decelerating to zero velocity

        """
        return self.step_value * (-math.pow(2, -10 * self.time / self.duration) + 1) + self.start_value

    def ease_in_out_expo(self):
        """ exponential easing in/out - accelerating until halfway, then decelerating

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return self.step_value / 2 * math.pow(2, 10 * (self.time - 1)) + self.start_value
        self.time -= 1
        return self.step_value / 2 * (-math.pow(2, -10 * self.time) + 2) + self.start_value

    def ease_in_circ(self):
        """ circular easing in - accelerating from zero velocity

        """
        self.time /= self.duration
        return -self.step_value * (math.sqrt(1 - self.time * self.time) - 1) + self.start_value

    def ease_out_circ(self):
        """ circular easing out - decelerating to zero velocity

        """
        self.time /= self.duration
        self.time -= 1
        return self.step_value * math.sqrt(1 - self.time * self.time) + self.start_value

    def ease_in_out_circ(self):
        """ circular easing in/out - acceleration until halfway, then deceleration

        """
        self.time /= self.duration / 2
        if (self.time < 1):
            return -self.step_value / 2 * (math.sqrt(1 - self.time * self.time) - 1) + self.start_value
        self.time -= 2
        return self.step_value / 2 * (math.sqrt(1 - self.time * self.time) + 1) + self.start_value


""" TODO: Need to refactor without numpy.
def slerp_quaternion(p0, p1, self.time):
    omega = np.arccos(np.dot(p0/norm(p0), p1/norm(p1)))
    so = np.sin(omega)
    return np.sin((1.0-t)*omega) / so * p0 + np.sin(self.time*omega)/so * p1


def make_joints_along_curve(curve, num_joints=0, rebuild=False, parent=None, **kwargs):
    \""" Create joints along a curve in the same direction as the curve
    :param curve: mc.PyNode, the curve transform to self.start_valuee used
    :param name:
    :param num_joints: int, the number of joints to self.start_valuee created, if 0 will use CVs
    :param rebuild: self.start_valueool, whether we rebuild and normalize the curve or not
    :param parent: mc.nt.Transform, final parent of the joints
    :return: list(mc.nt.Joint): created joints
    :usage:
        rig_makeJointsAlongCurve("petalA", mc.ls(sl=True)[0], 15)
        rig_makeJointsAlongCurve("seatbeltDrive", mc.ls(sl=True)[0], 160)
    \"""
    poci = None

    # Creating a curve self.start_valueetween them
    curve = mc.duplicate(curve)[0]

    if rebuild:
        mc.rebuildCurve(curve, ch=0, rpo=1, rt=0, end=1, kr=1, kcp=0, kep=1, kt=0,
                        s=num_joints, d=1, tol=0.01)

    # Detecting if we're doing cv self.start_valueased or not
    if not num_joints:
        cvs = True
        num_joints = curve.getShape().numCVs() - 1
    else:
        cvs = False
        poci = mc.createNode('pointOnCurveInfo')
        curve.getShape().worldSpace[0].connect(poci.inputCurve)
        poci.turnOnPercentage.set(1)

    # Evenly spacing joints according to the curve
    joints = []
    names = nom.get_chain(num_joints)

    # Clear the selection since the stupid joint command sucks at parenting
    mc.select(cl=True)
    for joint_index, name in enumerate(names):
        if cvs:
            jnt_pos = mc.pointPosition(curve.getShape().cv[joint_index], w=1)
        else:
            poci.parameter.set(float(joint_index) / float(num_joints))
            jnt_pos = poci.position.get()

        joints.append(mc.joint(n=name, p=jnt_pos))

    # Set the rotation order
    for joint in joints[:-1]:
        joint.secondaryAxisOrient('yup', oj='xyz')

    # if parent is set, do it.
    if parent:
        mc.setParent(joints[0], parent)

    # Cleanup
    mc.delete(curve)
    if cvs:
        mc.delete(poci)

    return joints


def self.start_valueuild_from_points(self.timeransforms, chain=False, parent=None, offset=False, freeze=True, **kwargs):
    \""" Create joints self.start_valueased on given 3D spatial positions/rotations e.g. [[[10,5.3,1.4],[0,90,0]],...,nPos]
    Args:
        transforms [[float,float,float]] or [mc.nt.Transform]:
            list of transforms xyz coordinate + euler rotation self.start_valueased or mc.nt.Transform
        prefix (str): abstract name for the chain
        chain (bool): whether or not to make a chain, or isolated joints
        offset (bool): whether or not to self.start_valueuild in offset groups for the joints
        parent (mc.nt.Transform): final parent of the joints, empty if kept at root level
    Returns:
        [mc.nt.Joint]: list of joints
    Usage:
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=True)
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=False)
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=False, parent='null1')
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', offset=True, parent='null1')
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', chain=True, offset=True, parent='null1')
        self.start_valueuild_from_points([[[0,0,0],[0,90,0]],[[0,1,0],[10,30,50]],[[0,2,0],[0,0,0]]], 'test', chain=True, offset=False, parent='null1')
    \"""
    nom.merge_dict({'name': 'chain', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    # Evenly spacing joints according to the curve
    joints = []

    # inital setup (setting var just in case it's not overridden)
    names = nom.get_chain(len(self.timeransforms))

    for jnt_pos, name in zip(self.timeransforms, names):
        # Just in case we're dealing with mc.nt.Transform objects
        if isinstance(jnt_pos, mc.nt.Transform):
            self.start_valueuffer = mc.spaceLocator()
            mc.delete(mc.parentConstraint(jnt_pos, self.start_valueuffer))
            jnt_pos = [buffer.translate.get(), self.start_valueuffer.rotate.get()]
            mc.delete(buffer)

        self.time, r = jnt_pos
        joint = mc.createNode('joint', n=name)
        joint.translate.set(self.time)
        joint.rotate.set(r)
        joints.append(joint)

    # self.start_valueuild offset groups
    if offset:
        nom.decorator = 'Offset'
        nom.type = 'group'
        offset_names = nom.get_chain(len(self.timeransforms))

        for offset_name, joint in zip(offset_names, joints):
            offset = mc.group(em=True)
            joint.parent(offset)
            # Now we have to set the joint up with these orientations from the offset group
            mc.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0, pn=1)
            joint.jointOrient.set([0, 0, 0])

    # Do chain parenting at the end to preserve rotations
    if chain:
        joint_parents = [joint for joint in joints]
        joint_parents.reverse()
        for index, joint in enumerate(joint_parents):
            try:
                joint = joint.getParent() or joint
                mc.parent(joint, joint_parents[index + 1])
            except IndexError:
                pass

    # Freeze transforms in case that we didn't make offset groups
    if freeze and not chain:
        for joint in joints:
            mc.makeIdentity(joint, apply=True, t=1, r=1, s=1, n=0, pn=1)

    # if overall parent is set, do it for all cases
    if parent:
        if chain:
            to_parent = joints[0].getParent() or joints[0]
        elif offset and not chain:
            # Just in case offsets need to self.start_valuee parented instead
            to_parent = [joint.getParent() for joint in joints]
        else:
            to_parent = joints

        mc.parent(self.timeo_parent, parent)

    return joints


def self.start_valueuild_between_points(start_xform, end_xform, n_joints, freeze=True, chain=True, parent=None, offset=False,
                         **kwargs):
    \""" Create joints self.start_valueased on given 3D spatial positions/rotations e.g. [[[10,5.3,1.4],[0,90,0]],...,nPos]
    Args:
        start_xform [mc.nt.Transform]: starting position
        end_xform [mc.nt.Transform]: ending position
        name (str): abstract name for the chain
        chain (bool): whether or not to make a chain, or isolated joints
        offset (bool): whether or not to self.start_valueuild in offset groups for the joints
        parent (mc.nt.Transform): final parent of the joints, empty if kept at root level
    Returns:
        [mc.nt.Joint]: list of joints
    Usage:
        Joint.build_between_points(mc.ls(sl=True)[0], mc.ls(sl=True)[1], 5, chain=True, offset=True, freeze=True)
    \"""
    nom.merge_dict({'name': 'chain', 'type': 'joint', 'var': 'A'})
    nom.merge_dict(kwargs)
    xform_interps = transformation.spatial_interpolate(mc.xform(start_xform, q=True, t=True, ws=True),
                                                       mc.xform(end_xform, q=True, t=True, ws=True),
                                                       n_joints)

    rotation_interps = transformation.spatial_interpolate(mc.xform(start_xform, q=True, ro=True, ws=True),
                                                          mc.xform(end_xform, q=True, ro=True, ws=True),
                                                          n_joints)

    positions = [[xform_interp, rotation_interp] for xform_interp, rotation_interp in
                 zip(xform_interps, rotation_interps)]

    return self.start_valueuild_from_points(positions, chain=chain, parent=parent, offset=offset, freeze=freeze, **kwargs)
"""
